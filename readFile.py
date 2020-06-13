def readConfig(filename, li):
	with open(filename,'r',encoding='utf-8') as fp:
		li.append(fp.read())

# 同时读取多个txt文件
files = ["key1.txt", "key2.txt", "key3.txt"]
result = []
for i in files:
	readConfig(i, result)
print(result)
