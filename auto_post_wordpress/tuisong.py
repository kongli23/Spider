import requests
import json


def tuisong(url):
    print('正在进行百度推送中....')
    jk = 'http://data.zz.baidu.com/urls?site=https://www.ncle.net&token=hf9ar3F0Cqi7qNYN'
    try:
        html = requests.post(jk,url).text
        html = json.loads(html)
        if html['success'] > 0:
            print("推送成功-----{}".format(html))
        else:
            print("推送失败-----{}".format(html))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    url = 'https://www.www.net/seo/410'
    tuisong(url)