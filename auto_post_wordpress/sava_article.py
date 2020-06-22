from auto_post_wordpress.wordpress_post import task
from auto_post_wordpress.split_tags import split_title
import threading

look = threading.Lock()

filenameList = []
# 保存html文件函数
def sava_html(title,article):
    filename = title

    # 过滤重复
    if filename not in filenameList:
        filenameList.append(filename)
        tags = split_title(filename)

        print('开始发布文章')
        dictInfo = {
            'domain': 'https://www.ncle.net',
            'loginUser': 'admin',
            'loginPass': 'xxxxxx',
            'category': 1,
            'wp_title': filename,
            'wp_content': article,
            'wp_tags': tags
        }
        task(dictInfo)