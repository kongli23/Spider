import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading

# 生产者队列，主要从每一页的url任务中解析图片下载链接，并添加到图片下载队列中
class Procuder(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'
    }

    # 因为使用中要传参，所以要重写init函数,使用 *args,**kwargs 代替父类的任意位置参数
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder, self).__init__(*args,**kwargs)
        # 创建自己的构造参数
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        # 不断的从队列中拿出url
        while True:
            # 判断每一页的队列中是否为空，如果为空跳出循环终止执行
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            # 将从队列中拿到的url进行解析
            self.parse_page(url)

    def parse_page(self,url):
        response = requests.get(url,headers=self.headers,timeout=30)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath('//div[@class="page-content text-center"]//img')
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            alt = re.sub(r'[\?？\.。!！\*/]','',alt)
            suffix = os.path.splitext(img_url)[1]
            filename = alt+suffix
            # 将解析出来的图片地址添加到图片下载队列中,传入两个参数：一个下载地址，一个文件名，使用元组代替
            self.img_queue.put((img_url,filename))

# 消费者队列，主要从图片下载队列中执行下载任务
class Consumer(threading.Thread):
    # 因为使用中要传参，所以要重写init函数,使用 *args,**kwargs 代替父类的任意位置参数
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        # 创建自己的构造参数
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        # 从图片下载队列中拿到数据
        while True:
            # 判断图片下载队列是否为空，并且判断生产图片队列是否为空，如果都为空，说明没有任务了，终止执行
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get() #此赋值方法会自动解包里面传递的元组参数，只要跟封包数据一致即可
            request.urlretrieve(img_url,'images/'+filename)
            print(filename+'  下载完成!')
def main():
    page_queue = Queue(100) #每一页的url
    img_queue = Queue(1000)   #图片队列

    for x in range(1,101):
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        page_queue.put(url) #将每一页的url添加到队列中

    # 创建生产者队列
    for x in range(15):
        t1 = Procuder(page_queue,img_queue)
        t1.start()

    # 创建消费者队列
    for x in range(15):
        t2 = Consumer(page_queue,img_queue)
        t2.start()

if __name__ == '__main__':
    main()