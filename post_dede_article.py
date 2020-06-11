import requests
import re
import datetime

# 定义账户域名信息
loginUser = 'admin'
loginPass = 'admin'
domain = 'http://pydede.com'

# 定义全局session 用来登录处理之后的发布等功能
session = requests.session()

loginHeader = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
# 先请求一次登录页面，拿到cookie
login_res = session.get(domain+'/dede/login.php?gotopage=%2Fdede%2F',headers=loginHeader)

# 开始post登录

# 登录之前首先要拿到验证码图片，之后再提交 post
res_img = session.get(domain+'/include/vdimgck.php')
imgpath = 'login.jpg'
picCode = res_img.content
# 将图片写入当前目录
with open(imgpath,'wb') as fp:
    fp.write(picCode)

# 保存图片到当前目录下
code = input('请输入验证码：')
print('输入的验证码为：'+code)

# 构造post参数
loginPostData = {
    'gotopage':'%2Fdede2F',
    'dopost':'login',
    'adminstyle':'newdedecms',
    'userid':loginUser,
    'pwd':loginPass,
    'validate':code,
    'sm1':''
}
loginPostHeader = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Content-Type':'application/x-www-form-urlencoded',
    'Referer':domain+'/dede/login.php?gotopage=%2Fdede%2F'
}
login_post = session.post(domain+'/dede/login.php',loginPostData,headers=loginPostHeader)

# 发布文章主要函数，传入分类id，标题，内容，标签
def post_article(cateid,post_title,post_content,post_tags):
    # 构造 post 内容
    curr_time = datetime.datetime.now()  # 获取当前时间
    post_time = curr_time.strftime('%Y-%m-%d %H:%M:%S')  # 将系统当前时间转换成字符串，并添加到post参数中
    params = {
        'channelid': (None, '1'),
        'dopost': (None, 'save'),
        'title': (None, post_title),    #文章标题
        'shorttitle': (None, ''),
        'redirecturl': (None, None),
        'tags': (None, post_tags),  #文章标签
        'weight': (None, 2),
        'picname': (None, None),
        'name="litpic"; filename=""': (None, None),
        'source': (None, None),
        'writer': (None, None),
        'typeid': (None, cateid),  # 分类ID
        'typeid2': (None, None),
        'keywords': (None, post_tags),  #文章关键词，跟标签一样
        'autokey': (None, 1),
        'description': (None, None),
        'dede_addonfields': (None, None),
        'imageField.x': (None, 27),
        'imageField.y': (None, 11),
        'remote': (None, 1),
        'autolitpic': (None, 1),
        'needwatermark': (None, 1),
        'sptype': (None, 'hand'),
        'spsize': (None, 5),
        'body': (None, post_content),   #文章内容
        'voteid': (None, None),
        'notpost': (None, 0),
        'click': (None, 118),
        'sortup': (None, 0),
        'color': (None, None),
        'arcrank': (None, 0),
        'money': (None, 0),
        'pubdate': (None, post_time),
        'ishtml': (None, 1),
        'filename': (None, None),
        'templet': (None, None)
    }

    postHeader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': domain+'/dede/article_add.php?channelid=1'
    }

    post_res = session.post(domain+'/dede/article_add.php', files=params, headers=postHeader)
    return post_res

# print(login_post.text)
if(login_post.text.find('成功登录') !=-1):
    print('登录成功!，等待进入后台...')
    admin_res = session.get(domain+'/dede/index.php')
    if(admin_res.text.find('欢迎使用') !=-1):
        print('您已成功进入网站后台，稍后获取分类!')

        # 提取栏目ID信息
        cate_res = session.get(domain+'/dede/article_add.php?channelid=1')
        pat_cate = "<option value='(\d+)' class='option\d+'>(.*?)</option>"
        temp_cate = re.compile(pat_cate).findall(cate_res.text)
        print('当前的分类信息为：'+str(temp_cate))
        cateid = int(input('请输入分类ID进行发布文章：'))
        print('您选择的分类ID是：'+str(cateid))

        # 获取发布标题，内容，标签
        post_title = input('请输入要发布的标题：')
        post_content = input('请输入要发布的内容：')
        post_tags = input('请输入要发布的标签，可以为空，使用英文逗号隔开：')
        print('您的标题是：'+post_title)
        print('您的内容是：' + post_content)
        print('您的标签是：' + post_tags)

        print('正在为您发布文章....')
        post_res = post_article(cateid=cateid,post_title=post_title,post_content=post_content,post_tags=post_tags)
        if(post_res.text.find('成功发布文章') !=-1):
            succ_link = re.compile(r"href='(.*?)' target='_blank").findall(post_res.text)
            link = succ_link[0]
            print('文章发布成功，地址是：'+domain+link)
        else:
            print('文章发布失败!'+post_res.text)
else:
    print('登录失败!'+login_post.text)