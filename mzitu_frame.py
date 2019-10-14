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

def __task(img_url,dir_name,index):
    while True:
        try:
            img_bs = helper.GetBs(img_url)
            img_source_url = img_bs.select('div.main-image')[0].p.img.get('src')
            #print(img_source_url)
            save_path = os.path.join(dir_name,"%d.%s"%(index+1,img_source_url.split('.')[-1]))
            #print(save_path)
            if not helper.DownloadFile(img_source_url,save_path,{"Referer":img_url}):continue
        except Exception as ex:
            #print(ex)
            continue
        #print("下载成功",img_url)
        break


def DownloadImage(url):
    bs = helper.GetBs(url)
    #print(bs)
    if not bs:
        #print("下载错误")
        return False

    try:
        dir_name = bs.select('.main-title')[0].text
        #print(dir_name)
        dir_tmp = dir_name
        try_count = 1
        while os.path.exists(dir_tmp):
            dir_tmp = "%s%d" % (dir_name,try_count)
            try_count += 1
        dir_name = dir_tmp
        try:
            os.mkdir(dir_name)
        except Exception:
            os.mkdir(str(uuid.uuid1()))

        img_num = int(bs.select('.pagenavi a')[-2].string)
        #print(img_num)
        pool = threadpool.ThreadPool(8)
        for i in range(img_num):
            img_url = "%s/%d" % (url,i+1)
            #print(img_url)
            req = threadpool.WorkRequest(__task,[img_url,dir_name,i])
            pool.putRequest(req)
        pool.wait()
        print(url,"下载完成")
        return True
    except Exception as ex:
        print("error",ex,"\t",url)
        return False

if __name__ == "__main__":
    url = r''
    if not url:
        argv = sys.argv
        if len(argv) == 1:
            print("请输入要下载的套图url")
            sys.exit(-1)
        url = argv[1]
    #print(url)
    print(DownloadImage(url))




