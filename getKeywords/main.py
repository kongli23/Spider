import requests
from lxml import etree
import threading
from queue import Queue

lock=threading.Condition() #创建线程锁
initial = ['gif图片']    #初始集合
existed = []    #已存在的

class Process_Html(threading.Thread):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.41'
    }
    def __init__(self,keyList_queue,*args,**kwargs):
        super(Process_Html, self).__init__(*args,**kwargs)
        self.keyList_queue = keyList_queue

    # 处理得到的html源码，从中提取关键词，并写入文件
    def run(self):
        down_url = 'https://www.baidu.com/s?wd={0}&pn=0'.format(self.keyList_queue.get())
        html = self.down_html(down_url)
        etree_obj = etree.HTML(html)
        table_th = etree_obj.xpath('//div[@id="rs"]/table//tr//th//text()')
        print('当前词根：'+str(table_th))
        if (len(table_th) > 0):
            for item in range(len(table_th)):
                # 过滤关键词，必须包含某词
                if 'gif' in table_th[item]:
                    # 如果已存在的集合中不存在该关键词则说明它是新的，则继续累加到任务集合中
                    if table_th[item] not in existed:
                        initial.append(table_th[item])

                        # 一直操作IO，不加锁，错误时文件内容乱码
                        lock.acquire()
                        # 将最新采集到的词追加写入文件中
                        with open('keyword.txt', "a", encoding='utf-8') as file:
                            file.write(table_th[item] + "\n")
                        lock.release()

        print('待采集：' + str(len(initial)))
        print('已得到：' + str(len(existed)))
        if(len(initial)>0):
            lock.acquire()
            runStart()
            lock.release()

    # 线程下载源码
    def down_html(self,url):
        text = ''
        try:
            # 获取源码
            str = requests.get(url, headers=self.headers, timeout=30)

            # 传递源码，提取关键词
            text = str.text

        except Exception as Err:
            print('异常：' + str(Err))
        return text

# 生成关键词采集url
def create_url(keyList_queue):
    process = Process_Html(keyList_queue)
    process.start()

def runStart():
    keyList_queue = Queue(1000)
    i = 0
    while i < len(initial):
        # print(initial[i])
        existed.append(initial[i])

        keyList_queue.put(initial[i])
        # create_url(initial[i])  #传递关键词生成采集url
        create_url(keyList_queue)
        initial.pop(i)
if __name__ == '__main__':
    runStart()