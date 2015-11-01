#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Queue
import threading
import time
import summary_plot
import file_util

exitFlag = 0
content_2_grams_list = []
jaccard_distance_list = []

class myThread (threading.Thread):
    def __init__(self, threadID, name, q, convert_lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.convert_lock = convert_lock

    def run(self):
        print "Starting " + self.name
        convert_list_to_grams(self.name, self.q)
        print "Exiting " + self.name


def convert_list_to_grams(threadName, q):
    """
    这个线程主要是负责把content_list的文本弄成2-grams的形式
    然后再添加到content_2_grams_list中
    """
    global content_2_grams_list
    while not exitFlag:
        if not workQueue.empty():
            # data = q.get()
            content_list = q.get()
            content_2_grams_list = content_2_grams_list + [summary_plot.get_2_grams(content) for content in content_list]
            print "%s processing %s" % (threadName, len(content_2_grams_list))
            queueLock.release()
        else:
            queueLock.release()

def compute_jaccard_distance(threadName, q):
    while not exitFlag:
        

fu = file_util.FileUtil()
fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew.mP')
fu.get_structure()
content_list = fu.get_content_list()[0:100]

threadList = ["Thread-1", "Thread-2", "Thread-3"]
# nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for i in range(0,100,10):
    workQueue.put(content_list[i:i+10])
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print len(content_2_grams_list)
print "Exiting Main Thread"
