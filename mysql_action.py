import pymysql

# mysql 操作常用命令
# ========================================================
# --创建表，添加主键，自动增长
# create table test(
# 	id int primary key auto_increment,
# 	title varchar(255),
# 	content text
# )
#
# --查询所有数据
# select * from test
#
# --新增数据
# insert into test(title,content) values('这是自动添加的标题2','我是内容我怕谁2')
#
# --指定查询
# select title,content from test where id = 1
#
# --删除数据
# delete from test where id=19
#
# --更新数据
# update test set title="我是标题，我要更新" where id=16
# ========================================================


# 创建链接字符串
conn = pymysql.connect(host='localhost',user='spider',password='spider',database='spider',port=3306)
# 创建游标，操作mysql必须得有这个
cursor = conn.cursor()

# insert 插入数据操作
# for i in range(10,20):
#     # 构建sql语句，此处的参数，不管是int 还是str 都得用 %s否则会报错
#     sql = "insert into test(title,content) values('{0}','{1}')".format('这是用pycharm动态插入的标题：'+str(i),'这是用pycharm动态插入的内容段')
#     # 执行sql语句
#     cursor.execute(sql)
#     # 提交要执行的sql命令
#     conn.commit()

# select 查询操作，三种方式
# 1.只返回一条数据
# sql = 'select title,content from test where id = {}'.format(3)
# cursor.execute(sql)
# result = cursor.fetchone()
# print(result)

# 2.返回多条数据
# sql = 'select title,content from test'
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)

# 3.指定返回几条数据
# sql = 'select title,content from test'
# cursor.execute(sql)
# result = cursor.fetchmany(3)    #里面的值给几就返回几条数据
# print(result)

# delele 删除操作
# sql = 'delete from test where id={}'.format(17) #里面的值给几就删除id为几的数据
# cursor.execute(sql)
# conn.commit()

# update 更新操作
sql = 'update test set title="{0}" where id={1}'.format('这个是要更新的标题',16) #把id为16的标题更改为这个新的标题
cursor.execute(sql)
conn.commit()

# 操作完毕必须关闭连接
conn.close()
