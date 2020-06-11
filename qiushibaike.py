import requests
from lxml import etree

class Qiushibaike():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    }
    pages = 0
    # 处理每一页源码，得到内容链接列表
    def get_page_list(self,url):
        resp = requests.get(url,headers=self.headers)
        html = etree.HTML(resp.text)
        detail_url = html.xpath('//a[@class="contentHerf"]/@href')
        self.parse_url_list(detail_url)

    # 处理得到的列表内容页url,获取内容页数据
    def parse_url_list(self,detail_url):
        for urls in detail_url:
            url = 'https://www.qiushibaike.com{}'.format(urls)
            resp = requests.get(url,self.headers)
            page = etree.HTML(resp.text)
            content = page.xpath('//div[@class="content"]/text()')
            duanzi_list = ','.join(content)
            self.pages = self.pages+1
            with open('duanzi.txt','a',encoding='utf-8') as file:
                file.write(str(self.pages)+'.'+duanzi_list+'\n')
                print('第：'+str(self.pages)+'条段子保存完毕!')
            print('-' * 30)

    # 生成列表链接 1 - 10页
    def spider(self):
        for page in range(1,11):
            url = 'https://www.qiushibaike.com/text/page/{}/'.format(page)
            print(url)
            self.get_page_list(url)

if __name__ == '__main__':
    duanzi = Qiushibaike()
    duanzi.spider()