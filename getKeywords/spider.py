import threading
import requests
from lxml import etree

# 初始词
gKeyList = []  #种子列表
with open('initial.txt', "r", encoding='utf-8') as file:
    for line in file:
        gKeyList.append(line.replace('\n', ''))

contain = []    #必须包含
with open('contain.txt', "r", encoding='utf-8') as file:
    for line in file:
        contain.append(line.replace('\n',''))

existed = []    #已存在

# 创建锁
look = threading.Lock()

# 生产者
class Producers(threading.Thread):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.41'
    }

    def run(self):
        while True:
            for key in gKeyList:
                # existed.append(key) #每采集一个记录一个，防止重复
                self.parse_key(key)

    def parse_key(self,key):
        url = 'https://www.baidu.com/s?wd={0}&pn=0'.format(key)
        try:
            str = requests.get(url, headers=self.headers, timeout=30)
            # 传递源码，提取关键词
            self.parse_html(str.text)
        except Exception as Err:
            print('异常：' + str(Err))

    def parse_html(self,text):
        etree_obj = etree.HTML(text)
        table_th = etree_obj.xpath('//div[@id="rs"]/table//tr//th//text()')

        for new_key in table_th:
            # 过滤关键词，必须包含
            for con in contain:
                # 必须包含某词，并且排除已存在的词，防止重复添加
                if con in new_key and new_key not in gKeyList:
                    gKeyList.append(new_key)
                    print('新词：{0}，总数：{1}'.format(new_key, len(gKeyList)))

                    # 写入文件
                    look.acquire()
                    with open('keywords.txt','a',encoding='utf-8') as fp:
                        fp.write(new_key+'\n')
                    look.release()
def main():
    # 创建5个生产者进行生产
    for x in range(10):
        t1 = Producers()
        t1.start()

if __name__ == '__main__':
    main()