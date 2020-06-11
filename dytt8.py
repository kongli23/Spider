import requests
from lxml import etree

class dytt8():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    }

    def get_detail_url(self,url):
        resp = requests.get(url,headers=self.headers)
        resp.encoding = 'gbk'
        # print(resp.text)
        html = etree.HTML(resp.text)
        detail_url = html.xpath('//div[@class="co_content8"]//table//a/@href')
        movie = self.parse_detail_url(detail_url)
        return movie

    def parse_detail_url(self,detail_url):
        for x in detail_url:
            url = 'https://www.dytt8.net{}'.format(x)
            resp = requests.get(url,self.headers)
            resp.encoding = 'gbk'
            text = resp.text
            html = etree.HTML(text)
            movie = {}
            title = html.xpath('//h1//text()')[0]
            movie['title'] = title  #标题
            zoom = html.xpath('//div[@id="Zoom"]')[0]
            imgs = zoom.xpath('.//img/@src')
            cover = imgs[0]
            # detail_img = imgs[1]
            movie['cover'] = cover  #主图
            # movie['detail_img'] = detail_img    #剧照

            infos = zoom.xpath('.//text()')
            for index,info in enumerate(infos):
                # print(info)
                # print('-' * 30)
                if info.startswith('◎译　　名'):
                    movie['years'] = info.replace('◎年　　代','').strip()   #年代
                if info.startswith('◎产　　地'):
                    movie['origin'] = info.replace('◎产　　地', '').strip()  # 产地
                if info.startswith('◎类　　别'):
                    movie['types'] = info.replace('◎类　　别', '').strip()  # 类型
                if info.startswith('◎上映日期'):
                    movie['release_date'] = info.replace('◎上映日期', '').strip()  # 上映日期
                if info.startswith('◎片　　长'):
                    movie['movie_length'] = info.replace('◎片　　长', '').strip()  # 片长
                if info.startswith('◎导　　演'):
                    movie['director'] = info.replace('◎导　　演', '').strip()  # 导演
                if info.startswith('◎编　　剧'):
                    movie['screenwriter'] = info.replace('◎编　　剧', '').strip()  # 编剧
                if info.startswith('◎主　　演'):
                    # movie['starring'] = info.replace('◎主　　演', '').strip()  # 主演
                    strring = info.replace('◎主　　演', '').strip()
                    actors = [strring]
                    for x in range(index+1,len(infos)):
                        actor = infos[x].strip()
                        if actor.startswith('◎'):
                            break
                        actors.append(actor)
                    movie['actors'] = actors    #主演
                if info.startswith('◎简　　介'):
                    # movie['introduction'] = info.replace('◎简　　介', '').strip()  # 简介
                    introductions = []
                    for x in range(index+1,len(infos)):
                        introduction = infos[x].strip()
                        if introduction.startswith('【下载地址】'):
                            break
                        introductions.append(introduction)
                    movie['introduction'] = introductions
            download_url = html.xpath('//td[@bgcolor="#fdfddf"]/a/@href')[0]
            movie['download_url'] = download_url
            return movie

    def spider(self):
        movies = []
        for x in range(1,10):
            url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(x)
            movie = self.get_detail_url(url)
            movies.append(movie)
            print(movies)

if __name__ == '__main__':
    dytt8 = dytt8()
    dytt8.spider()