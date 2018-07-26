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


def md5(s):
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()


cl_content_url = re.compile(r'(?<=http://www\.zxcs8\.com/post/)\d+')
cl_list_url = re.compile(r'http://www.zxcs8.com/sort/\d+')
domain = 'zxcs8.com'
cache = {
    'http://www.zxcs8.com/post/4267': True
}

f = open('db/zxcs_downloads.dat', mode='w', encoding="utf-8")


def write_down(s):
    print(s)
    f.write('%s\n' % s)
    f.flush()


def get_content(url, cache=True):
    f_name = 'db/%s.dat' % md5(url)
    if cache and os.path.exists(f_name):
        with open(f_name, mode='r', encoding='utf-8') as fs:
            return ''.join(fs.readlines())
    else:
        req = requests.get(url)
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
    a_tags = sel.xpath('//a')
    if not len(a_tags):
        return
    for a in a_tags:
        try:
            url = a.xpath('@href')[0]
            if url in cache:
                continue
            else:
                cache[url] = True
            match = cl_list_url.search(url)
            if match:
                '''
                    列表页
                '''
                deal_url(url)
                time.sleep(1)
                continue
            match = cl_content_url.search(url)
            if match:
                '''
                    详情页
                '''
                novel_name = a.xpath('text()')[0]
                download_txt('%s,http://www.zxcs8.com/download.php?id=%s' % (novel_name, match.group(0)))
                continue
        except:
            traceback.print_exc()


def download_txt(url):
    write_down(url)


if __name__ == '__main__':
    home_url = 'http://www.zxcs8.com/'
    deal_url(home_url)
