# Python3

import re
import urllib.request
import json
import math

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
base_url = 'http://bgm.tv/'
api_base_url = 'http://api.bgm.tv/'
name_pattern = '<a href=\"/subject/\d+\" class=\"l\">.*?</a'
rank_pattern = '</small>\d+</span'

def handle_rank_page(content):
    # <a href="/subject/253" class="l">星际牛仔</a

    res = re.findall(pattern=name_pattern, string=content)
    animes = []

    for i in range(len(res)):
        pos1 = res[i].find('t/')
        pos2 = res[i].rfind(' class')
        _id = res[i][pos1+2:pos2-1]
        pos3 = res[i].rfind('>')
        pos4 = res[i].rfind('<')
        name = res[i][pos3+1:pos4]
        animes.append({'id': _id, 'name': name})
    return animes


def cal_one_dev(bgm_id):
    url = api_base_url + 'subject/' + bgm_id
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode()
    dic = json.loads(data)
    # print(dic)
    count = dic['rating']['count']
    total = dic['rating']['total']
    avg = 0.0
    dev = 0.0
    for i in range(1,11):
        avg += i * count[str(i)]
    avg /= total
    for i in range(1,11):
        dev += count[str(i)] * (i-avg) * (i-avg)
    dev = math.sqrt(dev / total)
    # print('dev=', dev)
    return dev


def cal_all_dev():
    page = 2
    anime_list = []
    for i in range(page):
        url = base_url + 'anime/browser?sort=rank&page=%d' % (i+1)
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        # res = str(data)
        anime_list += handle_rank_page(data.decode())


    print('总共%d个' % len(anime_list))
    for anime in anime_list:
        print(anime['name'], cal_one_dev(anime['id']))


if __name__ == '__main__':
    # cal_one_dev('876')
    cal_all_dev()
