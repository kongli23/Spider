import threading

value = 0
look = threading.Lock()

def add_value():
    global value

    look.acquire()  #对for 进行上锁，防止数据混乱
    for x in range(1000000):
        value +=1   #更改当前全局变量的值，使用两个线程数量多的情况下会产生数据混乱，所以要加锁防止混乱
    look.release()  #执行完之后释放锁
    print('value:{}'.format(value))

def threadMain():
    for x in range(2):
        t1 = threading.Thread(target=add_value)
        t1.start()

if __name__ == '__main__':
    threadMain()