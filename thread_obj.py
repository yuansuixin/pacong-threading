# -*- coding:UTF-8 -*-
import threading

import time


class SingThread(threading.Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def run(self):
        for x in range(1,6):
            print('唱歌')
            time.sleep(1)

class DanceThread(threading.Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def run(self):
        for x in range(1,6):
            print('跳舞')
            time.sleep(1)


def main():
    t_sing = SingThread('sing')
    t_dance = DanceThread('dance')
    t_sing.start()
    t_dance.start()
    t_sing.join()
    t_dance.join()
    print('主线程结束')


    # lock = threading.Lock()
    # lock.acquire()
    # lock.release()

if __name__ == '__main__':
    main()










