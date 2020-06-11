import requests
import re
import threading

keywords = 'seo'
headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://image.baidu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

# 处理百度地址解密，得到超清大图
def decode_url(url):
    """
    对百度加密后的地址进行解码\n
    :param url:百度加密的url\n
    :return:解码后的url
    """
    table = {'w': "a", 'k': "b", 'v': "c", '1': "d", 'j': "e", 'u': "f", '2': "g", 'i': "h",
             't': "i", '3': "j", 'h': "k", 's': "l", '4': "m", 'g': "n", '5': "o", 'r': "p",
             'q': "q", '6': "r", 'f': "s", 'p': "t", '7': "u", 'e': "v", 'o': "w", '8': "1",
             'd': "2", 'n': "3", '9': "4", 'c': "5", 'm': "6", '0': "7",
             'b': "8", 'l': "9", 'a': "0", '_z2C$q': ":", "_z&e3B": ".", 'AzdH3F': "/"}
    url = re.sub(r'(?P<value>_z2C\$q|_z\&e3B|AzdH3F+)', lambda matched: table.get(matched.group('value')), url)
    return re.sub(r'(?P<value>[0-9a-w])', lambda matched: table.get(matched.group('value')), url)

# 下载线程函数 @picurl=图片地址
num=0   #计数
def thread_downImg(picurl):
    global num
    try:
        # 使用 requests 提取文件流的方式比urlretrieve较快
        img_req = requests.get(picurl,headers=headers,timeout=30)
        num = num + 1
        with open(f'images\\{num}.jpg', 'wb+') as f:
            f.write(img_req.content)

        print(f'第{num + 1}张图片下载成功')
        with open('imglinks.txt','a',encoding='utf-8') as img:
            img.write(str(picurl)+'\n')
    except Exception as err:
        print('第' + str({num + 1}) + '张图片下载出错！' + str(err))

#下拉加载
for i in range(50):
    print('当前正在下载第：'+str(i)+'页图片')
    params={
    'tn':'resultjson_com',
    'ipn':'rj',
    'ct':'201326592',
    'is':'',
    'fp':'result',
    'queryWord':keywords,
    'cl':'2',
    'lm':'-1',
    'ie':'utf-8',
    'oe':'utf-8',
    'adpicid':'',
    'st':'-1',
    'z':'',
    'ic':'',
    'hd':'',
    'latest':'',
    'copyright':'',
    'word':keywords,
    's':'',
    'se':'',
    'tab':'',
    'width':'',
    'height':'',
    'face':'0',
    'istype':'2',
    'qc':'',
    'nc':'1',
    'fr':'',
    'expermode':'',
    'force':'',
    'pn':f'{i*30}',
    'rn':'30',
    'gsm':'',
    '1578150791178':''
    }
    # json默认使用的是严谨格式，当跨语言传递数据时，就容易报出这个错误，所以加上 strict=False 来处理
    req=requests.get('https://image.baidu.com/search/acjson',params=params,headers=headers).json(strict=False)
    for objURL in req['data']:
        if 'objURL' in objURL:
            imgUrl = decode_url(objURL['objURL'])
            print('正在下载：'+imgUrl)
            threading.Thread(target=thread_downImg,args=(imgUrl,)).start()
print('所有任务下载完毕！')