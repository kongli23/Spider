import requests
import re

vid = 'euiuhsdyi8h20ck' #视频地址标识码，如：https://v.qq.com/x/cover/pttuqywq2rxe7er.html
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
}

# 得到视频放映室编号 varticle
init_res = requests.get('https://v.qq.com/x/cover/'+vid+'.html',headers=header)
pat_varticle = 'comment_id":"(.*?)"'
varticle = re.compile(pat_varticle).findall(init_res.text)[0] #此 编号 是视频产生的，获取评论地址需要带上它

# 构造提交参数
def pars(cursor=0):
    params = {
        'callback': '_varticle'+str(varticle)+'commentv2',
        'orinum': '10',
        'oriorder': 'o',
        'pageflag': '1',
        'cursor': str(cursor),
        'scorecursor': '0',
        'orirepnum': '2',
        'reporder': 'o',
        'reppageflag': '1',
        'source': '132',
        '_': '1578276178032'
    }

# 提取下一页id
def pat_comm(code):
    pat = 'last":"(.*?)"'  # 下一页的参数
    commPage = re.compile(pat).findall(code)
    return commPage[0]

# 提取评论内容
def pat_comment(code):
    pat_content = 'content":"(.*?)"'  # 评论内容
    commContent = re.compile(pat_content).findall(code)
    print(commContent)
    return commContent

# 初次访问评论地址，获取第一层的评论内容及下一页的 id 号
vurl = 'https://video.coral.qq.com/varticle/'+str(varticle)+'/comment/v2?callback=_varticle2610258155commentv2&orinum=10&oriorder=o&pageflag=1&cursor=0&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=1578276178032'
res = requests.get(vurl,headers=header)

com_page = pat_comm(res.text) #得到下一页 last id
pat_comment(res.text) #输出第一层的评论内容
print('初始commid：'+str(com_page))

# last 不为空说明还有下一页
while(com_page != ''):
    vurl_s = 'https://video.coral.qq.com/varticle/'+str(varticle)+'/comment/v2?callback=_varticle2610258155commentv2&orinum=10&oriorder=o&pageflag=1&cursor='+str(com_page)+'&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=1578276178035'
    resPage = requests.get(vurl_s,pars(com_page),headers=header)
    # print(resPage.text)
    com_pages = pat_comm(resPage.text)  # 提取下一页 last

    print('下一页：'+str(com_pages)) #输出下一页 commid
    # 如果下一页的值跟当前页的值一样，则跳出循环，否则将下一页的值继续赋值给上一页
    if(com_page == com_pages):
        break
    else:
        com_page = com_pages
    pat_comment(resPage.text) #输出评论内容