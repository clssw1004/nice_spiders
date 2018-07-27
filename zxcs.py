'''
知轩藏书爬虫
@author cuiwei
@date 2018-07-26
'''
import re
import traceback
import time
import requests
from lxml import etree
import base64
import hashlib
import os
import json

db_path = './db'
if not os.path.exists(db_path):
    os.makedirs(db_path)


def md5(s):
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()


f = open('zxcs_downloads.txt', mode='w', encoding="utf-8")
cl_content_url = re.compile(r'(?<=http://www\.zxcs8\.com/post/)\d+')
cl_list_url = re.compile(r'http://www\.zxcs8\.com/(sort|record|tag)/\S+')
cl_title = re.compile(r' - 知轩藏书')
domain = 'zxcs8.com'
cache = {
    'http://www.zxcs8.com/post/4267': True
}


def write_down(s):
    # print(s)
    f.write('%s\n' % s)
    f.flush()


def get_content(url, cache=True):
    f_name = 'db/%s.dat' % md5(url)
    if cache and os.path.exists(f_name):
        with open(f_name, mode='r', encoding='utf-8') as fs:
            return ''.join(fs.readlines())
    else:
        req = requests.get(url, timeout=10)
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        if cache:
            with open(f_name, 'w', encoding='utf-8') as fs:
                fs.write(content)
        return content


def deal_url(target_url):
    html = get_content(target_url)
    sel = etree.HTML(html)
    urls = sel.xpath('//a/@href')
    if not len(urls):
        return
    for url in urls:
        try:
            if url in cache:
                continue
            else:
                cache[url] = True
            match = cl_list_url.search(url)
            if match:
                '''
                    列表页
                '''
                print(url)
                deal_url(url)
                time.sleep(1)
                continue
            match = cl_content_url.search(url)
            if match:
                '''
                    详情页
                '''
                # novel_name = a.xpath('text()')[0]
                download_txt('http://www.zxcs8.com/download.php?id=%s' % (match.group(0)))
                continue
        except:
            traceback.print_exc()


def download_txt(url):
    write_down(url)


def download_txt_real(url, info):
    html = get_content(url)
    sel = etree.HTML(html)
    urls = sel.xpath("//span[@class='downfile']/a/@href")
    title = sel.xpath("//title/text()")[0]
    title = cl_title.sub('', title)
    print(title, urls)
    info[title] = urls


if __name__ == '__main__':
    home_url = 'http://www.zxcs8.com/map.html'
    deal_url(home_url)
    # info = dict()
    # lines = open('zxcs_downloads.txt', mode='r', encoding="utf-8").readlines()
    # for url in lines:
    #     if url:
    #         download_txt_real(url.strip(), info)
    #         with open('zxcs_files.dat', mode='w', encoding="utf-8") as db:
    #             db.write(json.dumps(info))
