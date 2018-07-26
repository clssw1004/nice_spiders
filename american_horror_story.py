import hashlib
import os
import re
from urllib import request

from bs4 import BeautifulSoup


def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


path = './db'
if not os.path.exists(path):
    os.makedirs(path)

# 美国恐怖故事全集下载页面
url = 'http://www.meijuck.com/lyjs/5284.html'
fpath = '%s/%s.dat' % (path, md5(url))
if os.path.exists(fpath):
    html = open(fpath, mode='r', encoding='utf-8').read()
else:
    response = request.urlopen(url)
    html = str(response.read(), 'utf-8')
    open(fpath, mode='w', encoding='utf-8').writelines(html)

soup = BeautifulSoup(html, 'lxml')
links = soup.find_all('a', attrs={'href': lambda h: h and h.startswith('ed2k')})
for l in links:
    print(l['href'])
