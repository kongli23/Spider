import requests
from lxml import etree
import re
import json
import random

# 未做分页，此次抓取只拿了一个列表页测试，难点在于价格跟评论，都是分别在不同的地址中提取，全部以json返回数据

# 定义 ua 列表，用来随机，测试时会出乱码跟302，加上不同的ua之后正常了，所以定义一个随机ua
uaList = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.31 (KHTML, like Gecko) Chrome/17.0.558.0 Safari/534.31 UCBrowser/10.9.3.727',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.31 (KHTML, like Gecko) Chrome/17.0.558.0 Safari/534.31',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050317 Firefox/1.0.2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/535.12 (KHTML, like Gecko) Chrome/18.0.966.0 Safari/535.12',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 QQBrowser/9.2.5584.400',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36 QQBrowser/9.1.4060.400',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.8.1000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 QQBrowser/9.2.5583.400',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36 LBBROWSER',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36',
]

baseUrl = 'https://list.jd.com/list.html?cat=1315,1343,9720#' #测试列表
headers = {
    'User-Agent':random.choice(uaList),
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
requests.packages.urllib3.disable_warnings() #忽略urllib3请求时产生的错误
res = requests.get(baseUrl,headers=headers,verify=False)    #得到baseUrl 列表页源码
print(res.text)

# 提取标题跟链接
etree_obj = etree.HTML(res.text)
title = etree_obj.xpath("//div[@id='plist']//div[@class='p-name p-name-type3' or @class='p-name']/a/em/text()") #标题
href = etree_obj.xpath("//div[@id='plist']//div[@class='p-name p-name-type3' or @class='p-name']/a/@href") #链接
# print(len(title))
# print(len(href))

# 根据商品链接提取商品价格
def getGoodsPrice(result_href):
    # 如果价格输出为 None 说明采集受限了，此时需要分析下面的 url 参数，咱就不搞了。。

    try:
        pat_skuid = re.compile('/(\d+).html').findall(result_href)
        # print(pat_skuid[0])
        priceLink = 'https://c0.3.cn/stock?skuId=' + str(pat_skuid[
                                                             0]) + '&area=19_1607_47388_0&venderId=1000087084&buyNum=1&choseSuitSkuIds=&cat=1315,1343,9720&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=978535765&ch=1&callback=jQuery7839650'

        requests.packages.urllib3.disable_warnings()  # 忽略urllib3请求时产生的错误
        # print('价格获取链接：' + priceLink)
        price_res = requests.get(priceLink, headers=headers, allow_redirects=False, verify=False)

        pat_price = 'stock":(.*?),"choseSuit'
        pat_temp_price = re.compile(pat_price).findall(price_res.text)
        priceJson = json.loads(pat_temp_price[0])
        # print(type(priceJson))
        # print(priceJson['jdPrice']['p'])  得到价格
        price = priceJson['jdPrice']['p']
        if(price !=''):
            return price
        else:
            return '获取异常'
    except Exception as errPrice:
        pass

# 根据商品链接提取商品评论数
def getGoodsComment(result_href):
    try:
        pat_skuid = re.compile('/(\d+).html').findall(result_href)
        # print(pat_skuid[0])
        comment_link = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + str(pat_skuid[0])
        requests.packages.urllib3.disable_warnings()  # 忽略urllib3请求时产生的错误
        # print('评论获取链接：' + comment_link)

        comment_res = requests.get(comment_link, headers=headers, allow_redirects=False, verify=False)
        pat_price = 'CommentsCount":(.*?)]'
        pat_temp_comment = re.compile(pat_price).findall(comment_res.text)
        # print('HTML：' + pat_temp_comment[0])
        commentJson = json.loads(pat_temp_comment[0].replace('[', ''))
        # print(type(commentJson))
        # print(commentJson['CommentCountStr']) #得到评论
        comment = commentJson['CommentCountStr']
        if(comment !=''):
            return comment
        else:
            return '获取异常'
    except Exception as errComment:
        pass

# 循环得到商品列表中的标题跟链接，并根据链接获取价格跟评论数
for t, h in zip(title, href):
    result_title = t.strip()
    result_href = h.strip()
    result_price = getGoodsPrice(result_href) #根据链接获取价格
    result_comment = getGoodsComment(result_href) #根据链接获取评论数
    print('标题：'+str(result_title)+'| 链接：'+str(result_href)+'| 价格：'+str(result_price)+'| 评论数：'+str(result_comment))

print('获取商品列表信息结束！')