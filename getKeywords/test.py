import requests
import threading
from lxml import etree

look = threading.Lock()
contain = ['gif','段子']    #必须包含词
used = []   #存储已采集的关键词

# 解析源码返回新的关键词列表
def parse_html(text):
    key_list = []
    etree_obj = etree.HTML(text)
    table_th = etree_obj.xpath('//div[@id="rs"]/table//tr//th//text()')

    if (len(table_th) > 0):
        for item in table_th:
            # 过滤关键词，必须包含某词
            for con in contain:
                if con in item:
                    if item not in used:

                        # 将过滤好的新词添加
                        key_list.append(item)
    return key_list

# 依据新的词下载源码
def down_html(url):
    key_list = []

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.41'
    }
    try:
        str = requests.get(url, headers=headers, timeout=30)
        # 传递源码，提取关键词
        key_list = parse_html(str.text)
    except Exception as Err:
        print('异常：' + str(Err))
    return key_list

# 处理得到的新词，例如过滤重复，判断是否包含某些词
def getNew_key(key):
    down_url = 'https://www.baidu.com/s?wd={0}&pn=0'.format(key)
    keyList = down_html(down_url)
    for newKey in keyList:
        print('新词：'+newKey)
        look.acquire()
        with open('keywords.txt','a',encoding='utf-8') as fp:
            fp.write(newKey+'\n')
        look.release()
    return keyList

# total = 0
# 死循环，不停的下载添加关键词
def down_key():
    # global total

    initail = ['gif', '段子大全']

    i = 0
    while i<len(initail):
        # total +=1
        print('当前采集词：{0}'.format(initail[i]))
        # 将已采集过的关键词存储，防止添加重复
        used.append(initail[i])

        # 返回最新的关键词列表
        keyList = getNew_key(initail[i])

        # 每遍历一次就删除一次采集过的词
        initail.pop(i)

        # 遍历新关键词列表，并添加到原有集合中，使程序不断的生产，添加
        if len(keyList) >0:
            for key in keyList:
                initail.append(key)

        # 死循环停止条件
        # if total >=10:
        #     break
if __name__ == '__main__':
    # down_key()
    t1 = threading.Thread(target=down_key)
    t1.start()