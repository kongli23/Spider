import re

title_list = []  # 标题列表
with open(r'lib\title.txt', "r", encoding='utf-8') as file:
    for line in file:
        title_list.append(line.replace('\n', ''))

content = ''
with open(r'lib\content.txt', "r", encoding='utf-8') as file:
    content = file.read()


for title in title_list:
    ts = title.split('_')
    article = content.replace('{{key}}',ts[0])
    # print(title+'\n'+article)
    with open(r'html\{}.html'.format(title), 'w', encoding='utf-8')as ws:
        ws.write(article)
print('写入完成！')