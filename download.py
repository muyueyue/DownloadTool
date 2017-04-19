#coding=utf-8
import threading
import requests
import time
from tqdm import tqdm
from time import sleep

class Download(object):

    'A multi-threading download tool'

    def __init__(self, url, threadNum):
        self.url = url
        if len('/home/jiahao/data/' + url.split('/')[-1]) > 64:
            self.name = '/home/jiahao/data/test'
        else:
            self.name = '/home/jiahao/data/' + url.split('/')[-1]
        self.threadNum = threadNum
        self.fileLenght = self.getLenght()

    def getLenght(self):
        respone = requests.head(self.url)
        return int(respone.headers['Content-Length'])

    def downloadThread(self, start, end):
        headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
        respone = requests.get(self.url, headers=headers, stream=True)
        #print ' start: %s end: %s' % (start, end)
        with open(self.name, "wb") as f:
            print '线程', threading.currentThread().getName().split('-')[-1]
            print " total: ", self.fileLenght, 'k'
            for data in tqdm(iterable=respone.iter_content(), total=self.fileLenght, unit='k'):
                sleep(0.0001)
                f.seek(start)
                f.write(data)


    def getRange(self):
        offset = int(self.fileLenght / self.threadNum)
        ran = []
        for num in range(self.threadNum):
            if num == self.threadNum - 1:
                ran.append((offset * num, self.fileLenght))
            else:
                ran.append((offset * num, offset * (num + 1)))
        return ran

    def main_download(self):
        self.fd = open(self.name, "wb")
        ran = self.getRange()
        print 'range: ', ran
        thread_list = []

        for i in ran:
            start, end = i
            thread = threading.Thread(target=self.downloadThread, args=(start, end))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            # 设置等待，避免上一个数据块还没写入，下一数据块对文件seek，会报错
            i.join()

        self.fd.close()

if __name__ == "__main__":
    start_time = time.time()
    tool = Download("https://bh2-3rd-miner.baijincdn.com/file/c1c4bd1b672b9699fcef603fce73a6a4?sdk_id=258&task_id=3726832458329620558&business_id=4097&bkt=p3-1400c1c4bd1b672b9699fcef603fce73a6a4ff3a161d00000096435a&xcode=8eece15011386a7e6ed657f21c41c3bd0fda57a9f69903e8ded0b7c77404c736&fid=2550443296-250528-2280583789&time=1492590949&sign=FDTAXGERLBHS-DCb740ccc5511e5e8fedcff06b081203-g8lktOPMyYfBcja4yX4HqN3xrrM%3D&to=z1&size=9847642&sta_dx=9847642&sta_cs=12392&sta_ft=zip&sta_ct=7&sta_mt=7&fm2=MH,Nanjing02,Netizen-anywhere,,jiangxi,cnc&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400c1c4bd1b672b9699fcef603fce73a6a4ff3a161d00000096435a&sl=83034191&expires=8h&rt=sh&r=368414928&mlogid=2520863848089910794&vuk=3227266362&vbdid=844878211&fin=%E8%B0%AD%E7%BB%B4%E7%BB%B4-%E5%A6%82%E6%9E%9C%E6%9C%89%E6%9D%A5%E7%94%9F.zip&fn=%E8%B0%AD%E7%BB%B4%E7%BB%B4-%E5%A6%82%E6%9E%9C%E6%9C%89%E6%9D%A5%E7%94%9F.zip&rtype=1&iv=0&dp-logid=2520863848089910794&dp-callid=0.1.1&hps=1&csl=300&csign=qTkBa2eudjGwUlgGg%2BpbCzEMw%2FI%3D&by=themis", 1)
    tool.main_download()
    tool.fd
    print '下载完成，花费的时间为: ', time.time() - start_time









