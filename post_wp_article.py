import requests
import re

# 配置登录的用户密码及操作的域名
loginUser = 'admin' #登录用户
loginPass = 'xxxx' #登录密码
domain = 'https://www.ncle.net' #操作的域名

# 登录header
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'wordpress_test_cookie=WP+Cookie+check',
    'Referer':domain+'/wp-login.php?redirect_to=http%3A%2F%2Fpytest.com%2Fwp-admin%2F&reauth=1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# 登录post参数
params = {
    'log':loginUser,
    'pwd':loginPass,
    'rememberme':'forever',
    'wp-submit':'登录',
    'redirect_to':domain,
    'testcookie':'1',
}

# 发布tag 文章如果需要添加标签，需要另外post才可以，所以先定义
def post_tages(nonce,tags):
    tagesID = []
    tagList = tags.split(',')
    for i in range(len(tagList)):
        # 构造POST标签，一个标签代表一个POST
        tagsData = {
            "name": str(tagList[i])
        }
        tagsHeader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'application/json, */*;q=0.1',
            'Referer': domain+'/wp-admin/post-new.php',
            'X-WP-Nonce': nonce,
            'Content-Type': 'application/json'
        }
        # 提交TAG
        tag_res = session.post(domain+'/index.php/wp-json/wp/v2/tags?_locale=user', params=tagsData,
                               headers=tagsHeader)
        # print('标签源码：'+tag_res.text)
        tag_ID = re.compile(r'id":(\d+),').findall(tag_res.text)  # 新的标签
        tag_ID1 = re.compile(r'term_id":(\d+)}').findall(tag_res.text)  # 添加的标签已存在
        if (len(tag_ID) > 0):
            tagesID.append(tag_ID[0])
        elif (len(tag_ID1) > 0):
            tagesID.append(tag_ID1[0])
    return tagesID

# 文章主要发布函数，传递获取的文章id，文章标识，标题，内容，分类id，标签进行发布文章
def post_article(postID,nonce,title,content,categoryID,tages):
    # 构造 post 参数
    postData = {
        "id": postID,
        "title": str(title),
        "content": "<!-- wp:paragraph -->\n<p>"+str(content)+"</p>\n<!-- /wp:paragraph -->",
        "categories": [categoryID],
        "tags": [','.join(tages)], "status": "publish"
    }

    # 发布文章时的 header 需要拼接少量参数，所以要单独定义
    postHeader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
        'Accept': 'application/json, */*;q=0.1',
        'Referer': domain+'/wp-admin/post.php?post=' + str(postID) + '&action=edit',
        'X-WP-Nonce': nonce,  # 这个参数是动态的，跟发布文章的id对应获取
        'X-HTTP-Method-Override': 'PUT',
        'Content-Type': 'application/json'
    }
    result = session.post(domain+'/index.php/wp-json/wp/v2/posts/' + str(postID) + '?_locale=user',
                          params=postData, headers=postHeader)
    # print('文章提交后的结果：'+str(result.text))
    result_code = re.compile('rendered":"(.*?)"').findall(result.text)  #提取成功地址

    succ_link = result_code[0].replace('\/', '/')   #转换地址中的 \/ 让它变成正常的 http://
    return succ_link

# 定义全局 session 进行get post 它会自动保存之前的cookie
session = requests.session()
res = session.post(domain+'/wp-login.php',params,headers=headers)
if(res.text.find('login_error') !=-1):
    print('输入的用户密码不正确')
else:
    # 如果没有出现密码不正确，说明可能登录成功了，接着去请求下后台，判断标识
    res_admin = session.get(domain+'/wp-admin/')
    if(res_admin.text.find('仪表盘') !=-1):    #找到标识 “仪表盘” 代表已经登录并进入了后台
        print('登录成功，稍后提取分类id')

        # 开始获取分类id
        category_res = session.get(domain+'/wp-admin/edit-tags.php?taxonomy=category')
        cateid = re.compile(r'<option class="level-0" value="(\d+)">(.*?)</option>').findall(category_res.text)
        print('当前网站分类如下，请输入数字编号发布文章：'+str(cateid))
        getcateID = int(input('请输入对应分类的数字ID：'))
        # print('输入的ID为：'+str(getcateID))

        # 发布文章前先要GET下发布页面，拿到生成的文章id
        res_id = session.get(domain+'/wp-admin/post-new.php') #带着登录的会话来访问发布页面，这样可以忽略 Cookie 问题
        temp_id = re.compile("name='post_ID' value='(\d+)'").findall(res_id.text)   #这个是发布文章生成的ID，一定要有它
        temp_nonce = re.compile('root":".*?nonce":"(.*?)"').findall(res_id.text)    #这个是发布文章的标识，一定要有它
        postID = temp_id[0]
        nonce = temp_nonce[0]

        # 开始POST
        posttitle = input('请输入发布的标题：')
        postcontent = input('请输入发布的内容：')
        posttags = input('请输入发布的标签，内容可以为空，使用英文逗号隔开：')
        print('输入的标题：'+posttitle)
        print('输入的内容：' + postcontent)
        print('输入的标签：' + posttags)

        # 发布文章要先发布标签，所以在此先拿到发布标签后的标签id
        tages_ID = post_tages(nonce=nonce,tags=posttags)

        # 构造POST数据，进行发布
        succ_link = post_article(postID=postID,nonce=nonce,title=posttitle,content=postcontent,categoryID=getcateID,tages=tages_ID)

        if(succ_link !=''):
            print('文章发布成功，地址是：'+succ_link)
        else:
            print('文章发布失败！')