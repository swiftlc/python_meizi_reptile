import requests
from bs4 import BeautifulSoup
import os
import shutil
import threading
import uuid
import time

url = 'http://www.mzitu.com'

main_folder = 'meizi'

if os.path.exists(main_folder):
    shutil.rmtree(main_folder)
os.mkdir(main_folder)



header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}


def DownloadImage(refer,folder_path,link,index):
    #print(folder_path,link,index)
    img_path = "{folder_path}/{index}.{ext}".format(folder_path=folder_path,index = index,ext=link.split('.')[-1])
    #print(img_path)
    _header = header.copy()
    _header['Referer'] = refer
    try:
        img_data = requests.get(link,headers=_header)
        with open(img_path,'wb') as f:
            f.write(img_data.content)
    except Exception:
        print('======================下载失败,等待重试')
        time.sleep(15)
        DownloadImage(refer,folder_path,link,index)



def DownloadFolder(title,link):
    """https://www.mzitu.com/205572/{page_index}"""
    #print('下载folder',title,link)
    try:
        page_data = requests.get(link,headers=header)
        page_soup = BeautifulSoup(page_data.text,'html.parser')
        max_page = int(page_soup.select('.pagenavi a')[-2].string)
    except Exception:
        print("重试下载folder",title)
        DownloadFolder(title,link)
        return 
    #print(max_page)

    #构建目录
    folder_path = os.path.join(main_folder,title)
    folder_path_tmp = folder_path
    index = 0
    while True:
        if not os.path.exists(folder_path_tmp):
            break
        index += 1
        folder_path_tmp = folder_path + str(index)
    folder_path = folder_path_tmp
    #print(folder_path)
    try:
        os.mkdir(folder_path)
    except Exception:
        folder_path = os.path.join(main_folder,str(uuid.uuid1()))
        os.mkdir(folder_path)

    for page_index in range(max_page):
        page_url = (link + '/{page_index}').format(page_index = page_index+1)
        #print(page_url)
        flag = False
        while True:
            try:
                page_data = requests.get(page_url,headers=header)
                page_soup = BeautifulSoup(page_data.text,'html.parser')
                #img_url = page_soup.find_all('img',attrs={"alt":title})[0].get('src')
                img_url = page_soup.select('div.main-image')[0].p.img.get('src')
                if flag:
                    print("重试成功,",page_url)
                #print(img_url)
                break
            except Exception:
                flag = True
                continue
        DownloadImage(page_url,folder_path,img_url,page_index + 1)


def DownloadPage(page):
    """page https://www.mzitu.com/page/{page_index}/"""

    page_url = "{host}/page/{page_index}/".format(host=url,page_index = page)
    #print('下载页面 ',page_url)


    try:
        page_data = requests.get(page_url,headers=header)
        page_soup = BeautifulSoup(page_data.text,'html.parser')
        all_li = page_soup.select('ul[id="pins"]>li')
    except Exception:
        return DownloadPage(page)

    #print('download_page',page)

    for li in all_li:
        if li.get('class') is None: #屏蔽广告
            href = li.a.get('href')
            title = li.a.img.get('alt')
            #print(href,title)
            #print("download_page_index",index)
            DownloadFolder(title,href)

def DownloadPageGroup(start,end):
    for x in range(start,end):
        DownloadPage(x)


try:
    #用get方法打开url并发送headers
    html = requests.get(url,headers = header)

    soup = BeautifulSoup(html.text,'html.parser')

    #max_page_str = soup.select('.next')[0].previous_sibling.previous_sibling.string    #通过兄弟节点
    max_page_str = soup.select('.nav-links a')[-2].string   #通过父子选择器
    #print(max_page_str)

    max_page = int(max_page_str)

    thread_num = 8

    num_per_thread = max_page//thread_num + 1

    thread_list = []
    for i in range(thread_num):
        start = i * num_per_thread + 1
        t = threading.Thread(target=DownloadPageGroup,kwargs={'start':start,'end':min(max_page + 1,start + num_per_thread)})
        t.start()
        thread_list.append(t)


    map(lambda t: t.join(),thread_list) 

except Exception as ex:
    print('error ',ex)

