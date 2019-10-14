import requests
from bs4 import BeautifulSoup
import os
import shutil
import threading
import uuid
import time
import sys
import threadpool



header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}


def MakeHeader(extra_header):
    return dict(header,**extra_header)
    
def GetContent(url,extra_header = None):
    if not extra_header:
        extra_header = {}
    h = MakeHeader(extra_header)
    #print(h)
    try:
        req = requests.get(url,headers=h)
        return req.content
    except Exception:
        return None

def DownloadFile(url,path,extra_header = None):
    content = GetContent(url,extra_header)
    if not content: return False
    f = None
    try:
        f = open(path,mode="wb")
        f.write(content)
    except Exception as ex:
        print(ex)
        return False
    finally:
        if f:f.close()
    return True


def GetBs(url,extra_header = None):
    content = GetContent(url,extra_header)
    if not content: return None
    try:
        bs = BeautifulSoup(content,"html.parser")
        return bs
    except Exception:
        return None


if __name__ == "__main__":
    pass
    #print(GetContent("https://www.mzitu.com/129674"))
    #print(DownloadFile("https://www.mzitu.com/129674","a"))
    #print(GetBs("https://www.mzitu.com/129674"))