import requests
import re
from auto_post_wordpress.tuisong import tuisong

# 定义全局 session 进行get post 它会自动保存之前的cookie
session = requests.session()


# 发布tag 文章如果需要添加标签，需要另外post才可以，所以先定义
def post_tages(domain,nonce,tags):
    print('正在发布文章tags')
    tagesID = []

    for i in range(len(tags)):

        # 构造POST标签，一个标签代表一个POST
        tagsData = {
            "name": str(tags[i])
        }
        tagsHeader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'application/json, */*;q=0.1',
            'Referer': domain+'/wp-admin/post-new.php',
            'X-WP-Nonce': nonce,
            'Content-Type': 'application/json'
        }
        try:
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
        except Exception as err:
            print('发布tag异常：'+str(err))
    print('tags发布完成....\\')
    return tagesID

# 文章主要发布函数，传递获取的文章id，文章标识，标题，内容，分类id，标签进行发布文章
def post_article(domain,postID,nonce,title,content,categoryID,tages):
    # print('正在发布文章：'+title)
    # print('正在发布内容：'+content)
    # print('正在发布tag：'+str(tages))
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

    succ_link = ''
    try:
        result = session.post(domain + '/index.php/wp-json/wp/v2/posts/' + str(postID) + '?_locale=user',
                              params=postData, headers=postHeader)

        # print('文章提交后的结果：'+str(result.text))
        result_code = re.compile('rendered":"(.*?)"').findall(result.text)  # 提取成功地址
        if len(result_code) >0:
            succ_link = result_code[0].replace('\/', '/')  # 转换地址中的 \/ 让它变成正常的 http://
            print('发布完成------------------->>>')

    except Exception as err:
        print('post发布文章异常：'+str(err))

    return succ_link

# 发布任务
def task(self):
    print('开始执行任务..../')
    domain = self['domain']
    # 登录header
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'wordpress_test_cookie=WP+Cookie+check',
        'Referer': domain + '/wp-login.php?redirect_to=http%3A%2F%2Fpytest.com%2Fwp-admin%2F&reauth=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    # 登录post参数
    params = {
        'log': self['loginUser'],
        'pwd': self['loginPass'],
        'rememberme': 'forever',
        'wp-submit': '登录',
        'redirect_to': domain,
        'testcookie': '1',
    }

    res = session.post(domain + '/wp-login.php', params, headers=headers)
    if (res.text.find('login_error') != -1):
        print('输入的用户密码不正确')
    else:
        # 如果没有出现密码不正确，说明可能登录成功了，接着去请求下后台，判断标识
        res_admin = session.get(domain + '/wp-admin/')
        if (res_admin.text.find('仪表盘') != -1):  # 找到标识 “仪表盘” 代表已经登录并进入了后台
            print('登录成功，稍后执行发布')

            # 开始获取分类id
            getcateID = self['category']

        try:
            # 发布文章前先要GET下发布页面，拿到生成的文章id
            res_id = session.get(domain + '/wp-admin/post-new.php')  # 带着登录的会话来访问发布页面，这样可以忽略 Cookie 问题
            temp_id = re.compile("name='post_ID' value='(\d+)'").findall(res_id.text)  # 这个是发布文章生成的ID，一定要有它
            temp_nonce = re.compile('root":".*?nonce":"(.*?)"').findall(res_id.text)  # 这个是发布文章的标识，一定要有它
            postID = temp_id[0]
            nonce = temp_nonce[0]

            # 开始POST
            posttitle = self['wp_title']
            postcontent = self['wp_content']
            posttags = self['wp_tags']

            # 发布文章要先发布标签，所以在此先拿到发布标签后的标签id
            tages_ID = post_tages(domain=domain,nonce=nonce, tags=posttags)

            # 构造POST数据，进行发布
            succ_link = post_article(domain=domain,postID=postID, nonce=nonce, title=posttitle, content=postcontent,
                                     categoryID=getcateID, tages=tages_ID)
            if (succ_link != ''):
                print('文章发布成功，地址是：' + succ_link)
                tuisong(succ_link)  #百度站长推送
            else:
                print('文章发布失败！')
        except Exception as err:
            print('发布文章异常：'+str(err))
if __name__ == '__main__':
    tags = ['经典幽默段子', '笑喷的段子', '一分钟笑掉大牙', '爆笑的笑话段子', '下载内涵段子最新版', '内涵段子视频', '笑破你肚子的笑话30个', '笑到肚痛的38个笑话', '让人捧腹大笑的段子']
    tags1= []
    dictInfo = {
        'domain': 'http://www.duanzi.io',
        'loginUser': 'admin',
        'loginPass': 'admin',
        'category': 1,
        'wp_title': '经典幽默段子搞笑文章0005',
        'wp_content': '经典幽默段子搞笑文章经典幽默段子搞笑文章经典幽默段子搞笑文章经典幽默段子搞笑文章',
        'wp_tags': tags
    }

    task(dictInfo)