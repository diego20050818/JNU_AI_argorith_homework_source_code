
import threading
import time
import random
from collections import deque

# 理发店的等待室座位数量
NUM_SEATS = 3

# 信号量初始化
customers = threading.Semaphore(0)
barber = threading.Semaphore(0)
mutex = threading.Lock()

# 等待室座位
free_seats = NUM_SEATS

def cut_hair(customer_id):
    print(f"理发师正在为顾客 {customer_id} 理发...")
    time.sleep(random.uniform(1, 2))
    print(f"顾客 {customer_id} 理完发了，帅气登场！")

def get_haircut(customer_id):
    print(f"顾客 {customer_id} 正在理发椅上等待理发...")

def barber_thread():
    global free_seats
    while True:
        customers.acquire()  # 等待顾客来
        with mutex:
            free_seats += 1  # 顾客进来腾出一个座位
            print(f"理发师被叫醒了！空座位 +1（剩余 {free_seats} 个）")
        barber.release()  # 通知顾客可以开始理发
        cut_hair(threading.current_thread().name)

def customer_thread(customer_id):
    global free_seats
    time.sleep(random.uniform(0.1, 1.5))  # 顾客随机到店
    with mutex:
        if free_seats > 0:
            free_seats -= 1
            print(f"顾客 {customer_id} 进入等待室（剩余 {free_seats} 个空位）")
            customers.release()  # 通知理发师
        else:
            print(f"顾客 {customer_id} 发现没座位，只好离开...")
            return
    barber.acquire()  # 等理发师叫号
    get_haircut(customer_id)

# 启动理发师线程
threading.Thread(target=barber_thread, name="理发师", daemon=True).start()

# 启动多个顾客线程
for i in range(10):
    threading.Thread(target=customer_thread, args=(i+1,), name=f"顾客{i+1}").start()

# 主线程保持运行
time.sleep(10)
