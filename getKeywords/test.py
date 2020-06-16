

# 解析源码返回新的关键词列表
def parse_html(text):
    pass

# 依据新的词下载源码
def down_html(url):
    # parse_html()
    pass

# 处理得到的新词，例如过滤重复，判断是否包含某些词
def getNew_key(key):
    keyList = []
    # down_html()
    for x in range(10):
        keyList.append(key+str(x))
    return keyList

# total = 0
# 死循环，不停的下载添加关键词
def down_key():
    global total

    initail = ['seo', 'seo优化']

    i = 0
    while i<len(initail):
        # total +=1
        print('当前词：{0}'.format(initail[i]))

        # 返回最新的关键词列表
        keyList = getNew_key(initail[i])

        # 每遍历一次就删除一次采集过的词
        initail.pop(i)

        # 遍历新关键词列表，并添加到原有集合中，使程序不断的生产，添加
        if len(keyList) >0:
            for key in keyList:
                initail.append(key)

        # 死循环停止条件
        # if total >=10:
        #     break
if __name__ == '__main__':
    down_key()