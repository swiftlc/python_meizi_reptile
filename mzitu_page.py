import requests
from bs4 import BeautifulSoup
import os
import shutil
import threading
import uuid
import time
import sys
import helper
import threadpool


import mzitu_frame

def __task(url):
    #print(url)
    while not mzitu_frame.DownloadImage(url):pass

def DownloadImagePage(url):
    bs = helper.GetBs(url)
    #print(bs)
    if not bs:return False
    try:
        all_li = bs.select('ul[id="pins"]>li')
        pool = threadpool.ThreadPool(8)
        for li in all_li:
            if li.get('class') is None: #屏蔽广告
                href = li.a.get('href')
                title = li.a.img.get('alt')
                #print(href,title)
                req = threadpool.WorkRequest(__task,[href])
                pool.putRequest(req)
        pool.wait()
        print(url,"整页下载完成")
        return True
    except Exception as ex:
        print(ex)
        return False        



if __name__ == "__main__":
    url = r''
    if not url:
        argv = sys.argv
        if len(argv) == 1:
            print("请输入page url")
            sys.exit(-1)
        url = argv[1]
    #print(url)
    print(DownloadImagePage(url))
    print("download over")