import pymongo

# 创建连接对象，端口号是固定默认的
client = pymongo.MongoClient('127.0.0.1',port=27017)

# 以连接对象来获取数据库,如果当前数据库不存也没有关系，它会自动创建
db = client.spider

# 获取数据库中的集合，也是就是其它数据库中的表
collection = db.qa

# 写入数据，写入的数据一般是json格式，{'key':'value'}，字典数据

# 插入一条数据
# collection.insert_one({"username":"张三"})

# 插入多条数据
# collection.insert_many([
#     {
#         'username':'王五',
#         'age':48
#     },
#     {
#         'username':'二狗',
#         'age':68
#     }
# ])

# 查找数据,find() 是获取所有的数据
# cursor = collection.find()
# for x in cursor:
#     print(x)

# 获取集合中的一条数据，它可以根据条件查询，
# 例如：result = collection.find_one({'age':18})   获取age=18的数据
# result = collection.find_one({'age':48})
# print(result)

# 只更新一条数据，它必须要给一个更新条件，默认会从集合中查找，从上往下，只更新一个
#前面的{'username':'张三'}是要更新的字段，后面是新的内容，中间用$set分割
# collection.update_one({'username':'张三'},{'$set':{'username':'王老六'}})

# 同时更新多条数据
# collection.update_many({'username':'王老六'},{'$set':{'username':'王八'}})

# 删除一条数据
# collection.delete_one({'username':'二狗'})

# 删除多条数据
# collection.delete_many({'username':'王八'})