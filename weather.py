import requests
from bs4 import BeautifulSoup

def pages_parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    }
    resp = requests.get(url,headers=headers)
    text = resp.content.decode('utf-8') #手动解码
    bs4 = BeautifulSoup(text,'html5lib')
    conMidtab = bs4.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_id = tds[0]
            if index == 0:
                city_id = tds[1]
            city = list(city_id.stripped_strings)[0]

            temps = tds[-2]
            temp = list(temps.stripped_strings)[0]

            print({'city':city,'temp':temp})
        print('-' * 50)
def main():
    urls = ['http://www.weather.com.cn/textFC/hb.shtml','http://www.weather.com.cn/textFC/db.shtml','http://www.weather.com.cn/textFC/hd.shtml','http://www.weather.com.cn/textFC/hz.shtml','http://www.weather.com.cn/textFC/hn.shtml','http://www.weather.com.cn/textFC/xb.shtml','http://www.weather.com.cn/textFC/xn.shtml','http://www.weather.com.cn/textFC/gat.shtml']
    for url in urls:
        pages_parse(url)

if __name__ == '__main__':
    main()
