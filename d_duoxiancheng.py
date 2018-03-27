# -*- coding:UTF-8 -*-
import json
import threading
import requests
from queue import Queue
from lxml import etree

# 使用多线程爬取fanjian网站的段子

g_crawl_flag=True
g_parse_flag = True

class  CrawlThread(threading.Thread):
    def __init__(self,name,page_queue,data_queue):
        super().__init__()
        self.name = name
        # 成员属性
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }

    def run(self):
        print('%s----线程启动'%self.name)
        while g_crawl_flag:
            url = 'http://www.fanjian.net/duanzi-'
            page = self.page_queue.get()
            url = url+str(page)
            r = requests.get(url=url,headers=self.headers)
            self.data_queue.put(r.text)
        print('%s----线程结束'%self.name)


class ParseThread(threading.Thread):
    def __init__(self,name,date_queue,fp,lock):
        super().__init__()
        self.name = name
        self.data_queue = date_queue
        self.fp = fp
        self.lock = lock

    def run(self):
        print('%s----线程开始' % self.name)
        while g_parse_flag:
            text = self.data_queue.get()
            self.parse_text(text)
        print('%s----线程结束' % self.name)
    def parse_text(self,text):
        tree  = etree.HTML(text)
        li_list = tree.xpath('//ul[@class="cont-list joke-list"]/li')
        items=[]
        for li in li_list:
            item={}
            try:
                image_url = li.xpath('.//img[@class="lazy"]/@data-src')[0]
                print(image_url)
                name = li.xpath('.//div[@class="joke-list-name"]/a[1]/@title')[0]
                content = li.xpath('.//div[@class="cont-list-main"]/div/text()')[0]
            except Exception as e:
                image_url=None
                name='匿名用户'
                content = None
            item={
                'image_url':image_url,
                'name':name,
                'content':content
            }
            items.append(item)
            # 写入文件
        self.lock.acquire()
        string = json.dumps(items,ensure_ascii=False)
        self.fp.write(string)
        # 释放锁
        self.lock.release()


def create_queue():
    page_queue = Queue()
    # 将所有的页码添加到队列中
    for page in range(1,3):
        page_queue.put(page)
    data_queue = Queue()
    return page_queue,data_queue

# 创建多个采集线程
def create_craw_thread(crawl_thread_list,page_queue,data_queue):
    crawl_name_list = ['采集线程1','采集线程2']
    for name in crawl_name_list:
        t_crawl = CrawlThread(name,page_queue,data_queue)
        t_crawl.start()
        # 将每次创建的线程保存到列表中
        crawl_thread_list.append(t_crawl)
    while g_crawl_flag:
        if page_queue.empty():
            global g_crawl_flag
            g_crawl_flag = False

# 创建解析线程
def create_parse_thread(parse_thread_list,data_queue,fp,lock):
    parse_name_list = ['解析线程1','解析线程2']
    for name in parse_name_list:
        t_parse = ParseThread(name,data_queue,fp,lock=lock)
        t_parse.start()
        parse_thread_list.append(t_parse)

    while g_parse_flag:
        if data_queue.empty():
            global g_parse_flag
            g_parse_flag = False
            break

def main():
    # 保存所有的爬取线程
    crawl_thread_list = []
    # 保存所有的解析线程
    parse_thread_list=[]
    # 创建两个队列，页码队列，数据队列
    page_queue,data_queue = create_queue()
    # 创建多个爬取的线程
    create_craw_thread(crawl_thread_list,page_queue,data_queue)

    # 写入到这个文件中，需要锁
    fp = open('duanzi.txt','a',encoding='utf-8')
    lock = threading.Lock()
    # 开辟多个解析线程
    create_parse_thread(parse_thread_list,data_queue,fp,lock)
    # 主线程等待所有线程结束之后再结束
    for t in crawl_thread_list:
        t.join()
    for t in parse_thread_list:
        t.join()

    fp.close()
    print('主线程结束')

if __name__ == '__main__':
    main()
















