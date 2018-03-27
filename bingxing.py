# -*- coding:UTF-8 -*-

# 先来回顾一下线程
import threading
import time


def sing():
    for x in range(1,5):
        print('我再唱歌')
        time.sleep(1)



def dance():
    for x in range(1,6):
        print('我再跳舞')
        time.sleep(1)


def main():
    t_sing = threading.Thread(target=sing,name='sing')
    t_dance = threading.Thread(target=dance,name='dance')

    t_sing.start()
    t_dance.start()
    # 让主线程等待子线程结束之后再结束
    t_sing.join()
    t_dance.join()
    print('主线程结束')

if __name__ == '__main__':
    main()







