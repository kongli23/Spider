import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading

# 使用Queue 结合生产者，消费者队列抓取图片

# 生产者
class Producers(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producers, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            # 判断如果页面列队为空，则跳出循环
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)
    
    def parse_page(self,url):
        resp = requests.get(url,headers=self.headers)
        text = resp.text
        html = etree.HTML(text)
        imgs = html.xpath('//div[@class="tagbqppdiv"]//a//img')
        for x in imgs:
            img_url = x.get('data-original')
            alt = x.get('alt')
            alt = re.sub(r'[:\.\*\?？。]','',alt)
            suffix = os.path.splitext(img_url)[1]
            filename = alt+suffix
            self.img_queue.put((img_url,filename))

# 消费者
class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            # 判断，如果图片下载队列为空，并且，循环遍历列表队列为空，则跳出循环
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, filename = self.img_queue.get()
            request.urlretrieve(img_url, 'img/' + filename)
            print(filename + '   下载完成！')

def main():
    page_queue = Queue(100) #创建100个队列，即一页一队列
    img_queue = Queue(1000) #创建1000个图片下载队列

    for x in range(200):
        url = 'https://www.fabiaoqing.com/biaoqing/lists/page/{0}.html'.format(x)
        # 将待遍历页面添加到页面队列中
        page_queue.put(url)

    # 创建5个生产者
    for x in range(5):
        t1 = Producers(page_queue,img_queue)
        t1.start()

    # 创建5个消费者
    for x in range(5):
        t2 = Consumer(page_queue,img_queue)
        t2.start()

if __name__ == '__main__':
    main()