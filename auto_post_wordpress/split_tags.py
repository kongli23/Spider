import requests
import re

def split_title(title):

    tags = []
    data = {
        'key':title,
        'submit':'查询'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.41',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.78901.net/sm-fenci/'
    }
    print('正在提取标题tags')
    try:
        resp = requests.post('http://www.78901.net/sm-fenci/', data=data, headers=headers)
        resp.encoding = 'utf-8'
        text = resp.text
        tags_pat = re.compile('</font>(.*?)</div>').findall(text)
        tags_str = '|'.join(tags_pat)
        tags_split = tags_str.split('|')
        tags_split_norepeat = list(set(tags_split))
        for x in tags_split_norepeat:
            if len(x) >= 5 and len(x) <= 15:
                tags.append(x.strip())
    except Exception as err:
        print('提取tag异常！'+str(err))

    print('tags提取完毕!')
    return tags

if __name__ == '__main__':
    tags = split_title('网站内部如何布局长尾关键词？(网站排名建设)')
    print(tags)