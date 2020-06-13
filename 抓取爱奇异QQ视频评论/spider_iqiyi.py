import requests
import re
import json

baseUrl = 'https://www.iqiyi.com/v_19rsho7kz8.html'

# 示例测试地址：https://www.iqiyi.com/v_19rsho7kz8.html，提取的评论是从页面底部全部评论开始，也是最新的
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept':'*/*',
    'Referer':baseUrl
}

temp_res = requests.get(baseUrl,headers=headers)
temp_tvid = re.compile(r'tvid=(\d+)&').findall(temp_res.text)
tvID = temp_tvid[0]

lastID = '' #下一页ID
isLoop = True #控制是否继续，貌似多余
pages = 1 #页面计数

# 提交参数拼接函数
def func_params(last_id):
    params = {
        'agent_type': '118',
        'agent_version': '9.11.5',
        'authcookie': 'null',
        'business_type': '17',
        'content_id': str(tvID), #此id 是视频 id, 2164623000
        'hot_size': '0',
        'last_id': last_id,
        'page': '',
        'page_size': '20',
        'types': 'time',
        'callback': 'jsonp_1578377334653_89867'
    }
    return params

url = 'https://sns-comment.iqiyi.com/v3/comment/get_comments.action?'

# 传递解析好的json字典，返回LastID 用于下一页请求
def getLastID(jsonLast):
    global lastID
    global isLoop
    global pages
    idList = []
    for content in jsonLast['comments']:
        idList.append(content['id']) #将所有ID放进集合中，以便后面提取最后一数据
        try:
            print(content['content']) #此处输出加个异常进行忽略，测试时发现偶尔会中断，貌似是content有问题，不影响整体
        except Exception as err:
            print('当前输出评论出错！'+str(err))
    print(idList)
    currentID = idList[-1] #每次只取最后一位id
    if(lastID == currentID): #如果最后的ID跟当前相同则跳出，控制采集页数可在此控制
        isLoop = False
    else:
        lastID = currentID
    print('第：'+str(pages)+'页评论获取完毕!----->>>')
    print('\n')
    pages = pages + 1

# 传递原始 html 代码，返回标准 json 字典
def getJsonData(code):
    pat = 'data":(.*?),"code'
    jsonData = re.compile(pat).findall(code) #得到标准json格式数据
    jsonObj = json.loads(jsonData[0]) #将json格式数据转为字典，只有字典才可以循环读取内容，本次抓取就学了这一个，难搞..
    print(type(jsonObj)) #打印当前类型，查看是否为字典
    getLastID(jsonObj)

# 第一次请求传空 lastid
params = func_params('')
req = requests.get(url=url,params=params,headers=headers)
getJsonData(req.text)
# print(req.text)

print('最后一位ID：'+lastID)
# lastid 不为空，则一直循环
while(lastID !='' and isLoop == True):
    params = func_params(lastID)
    req2 = requests.get(url=url, params=params, headers=headers)
    getJsonData(req2.text)