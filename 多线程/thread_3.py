import threading
import time
import random

# 初始值
gMoney = 1000

# 生产总值
gTotal_Loop = 10

# 当前产生的数量值
gLoop = 0

# 创建锁，使用Condition类，它比Look()性能更优
gCondition = threading.Condition()

# 生产者
class Producers(threading.Thread):
    def run(self):
        global gMoney
        global gLoop
        while True:
            money = random.randint(100,1000)    #随机产生100-1000的数，并添加到初值当中

            gCondition.acquire()
            # 判断，如果生产数值大于等于总数值，则退出循环
            if gLoop >= gTotal_Loop:
                gCondition.release()
                break
            gMoney += money
            print('生产了：{0}，剩余：{1}'.format(money,gMoney))
            gLoop += 1  #每生产一次，数值就+1
            gCondition.notify_all()  #通知阻塞的线程
            gCondition.release()
            time.sleep(0.5)
# 消费者
class Consumer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100,1000)

            gCondition.acquire()
            while gMoney < money:
                if gLoop >= gTotal_Loop:
                    gCondition.release()
                    return
                gCondition.wait()    #阻塞线程
            gMoney -= money
            print('消费了：{0}，剩余：{1}'.format(money,gMoney))
            gCondition.release()
            time.sleep(0.5)

def main():
    # 创建3个消费者，进行消费
    for x in range(3):
        t1 = Consumer()
        t1.start()

    # 创建5个生产者进行生产
    for x in range(5):
        t1 = Producers()
        t1.start()

if __name__ == '__main__':
    main()