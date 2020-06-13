import requests
from lxml import etree

success_ip = []
def getProxyIP():
    # url = 'http://www.xicidaili.com'
    url = 'https://www.xicidaili.com/wt/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edg/79.0.309.54'}
    response = requests.get(url, headers=header)
    # print(len(response.text))

    # 创建一个 etree 对象，传入待分析的文本
    etree_obj = etree.HTML(response.text)
    ip_list = etree_obj.xpath('//tr[@class="odd"]')  # 得到所有 ip信息
    item = []

    # 循环从 tr 列表中读取第 0 行的， 第2个td(ip)、第3个td(port)
    for ip in ip_list:
        ip_ = ip.xpath('./td[2]/text()')[0]
        port_ = ip.xpath('./td[3]/text()')[0]

        ips = ip_ + ':' + port_
        item.append(ips)

        # 取要 80 端口 ip
        # if(port_ =='80'):
        #     ips = ip_ + ':' + port_
        #     item.append(ips)
    print('ip提取完毕！ 等待验证活性')

    print('开始验证活性..')
    # 遍历访问，检测IP活性
    for it in item:
        # 因为并不是每个IP都是能用，所以要进行异常处理
        try:
            proxy = {
                'http': it
            }
            url1 = 'https://www.baidu.com/'
            # 遍历时，利用访问百度，设定timeout=1,即在1秒内，未送到响应就断开连接
            res = requests.get(url=url1, proxies=proxy, headers=header, timeout=1)

            # 打印检测信息，elapsed.total_seconds()获取响应的时间
            #print(it +'--',res.elapsed.total_seconds())
            success_ip.append(it)
        except BaseException as e:
            print(e)
    print('验证完毕')
    # print(success_ip)
    return success_ip

print(getProxyIP())