import requests
import json
import re

class Get_Movie():
    headers = {
        'Referer': 'https://movie.douban.com/explore',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.44'
    }
    def spider_page_list(self,url):
        resp = requests.get(url,headers=self.headers)
        jsonList = json.loads(resp.text)
        for info in jsonList['subjects']:
            self.parse_detail_page(info['url'],info['cover'])

    def parse_detail_page(self,url,cover):
        info_url = re.compile('(\d+)').findall(url)
        detail_url = 'https://movie.douban.com/j/subject_abstract?subject_id={}'.format(info_url[0])
        html = requests.get(detail_url,headers=self.headers)
        info_dict = html.json()

        movie_infos = []
        title = info_dict['subject']['title']
        directors = info_dict['subject']['directors']
        actors = info_dict['subject']['actors']
        duration = info_dict['subject']['duration']
        region = info_dict['subject']['region']
        types = info_dict['subject']['types']
        release_year = info_dict['subject']['release_year']
        movie_info = {
            '海报':cover,
            '片名':title,
            '导演':directors,
            '主演':actors,
            '类型':types,
            '片长':duration,
            '制片国家':region,
            '上映日期':release_year
        }
        movie_infos.append(movie_info)
        # return movie_infos
        print(movie_infos)

    def spider(self):
        base_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={0}'
        page = 0
        for x in range(0,10):
            url = base_url.format(page)
            self.spider_page_list(url)
            page = page + 20

if __name__ == '__main__':
    movie = Get_Movie()
    movie.spider()