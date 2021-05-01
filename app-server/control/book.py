# coding: utf-8
# coding=gbk
from lxml import etree

import requests
import json
from bs4 import BeautifulSoup


# 图书馆网址       ---需登录校园网
detailurl = 'http://opac.hytc.edu.cn:8080/opac/'
whereurl = 'http://opac.hytc.edu.cn:8080/opac/ajax_'
def findBook_func(value):
    # 获取网页源码
    def GetHtmlText(url):
        header = {
            'Accept': 'textml, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            #'Cookie': 'PHPSESSID=4ebqukv4mu5r4j7mjmm4or3d73',
            'Host': 'opac.hytc.edu.cn:8080',
            'Referer': 'http://opac.hytc.edu.cn:8080/opac/openlink.php?strSearchType=title&historyCount=1&strText=%E4%B8%89%E4%BD%93&doctype=ALL',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            r=requests.get(url,timeout=30,headers=header)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            return r.text
        except:
            return "访问失败"

    def GetWhere(url):
        r = GetHtmlText(url)
        xpathHtml = etree.HTML(r)
        Wheres=xpathHtml.xpath('//tr[@class="whitetext"]')
        resultlist=[]
        for w in Wheres:
            num=w[1].xpath('./text()')
            year = w[2].xpath('./text()')
            address=w[3].xpath('./text()')
            state=w[4].xpath('./font/text()')
            j={'num':num,'year':year,'address':address,'state':state}
            resultlist.append(j)
        return resultlist

    # 获取目标搜素所有图书
    def GetAllbook(bookname):
        bookDetailList=[]
        firsturl='http://opac.hytc.edu.cn:8080/opac/openlink.php?s2_type=title&s2_text=%E6%95%B0%E5%AD%A6&search_bar=new&title=%E6%95%B0%E5%AD%A6&doctype=ALL&with_ebook=off&match_flag=forward&showmode=list&location=ALL'
        # 字符串拼接，加入bookname
        htmlurl = 'http://opac.hytc.edu.cn:8080/opac/openlink.php?location=ALL&title='+bookname+'&doctype=ALL&lang_code=ALL&match_flag=forward&displaypg=20&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=no&count=2298&with_ebook=off&page='
        r=GetHtmlText(firsturl)
        # r = GetHtmlText(htmlurl)
        # 解析该源码
        xpathHtml=etree.HTML(r)

        #xPath解析语法
        allpage =int(xpathHtml.xpath('//span[@class="num_prev"]/b/font')[1].xpath('./text()')[0])
        print("allpage:",allpage)

        for page in range(1,2):
            r = GetHtmlText(htmlurl + str(page))
            xpathHtml = etree.HTML(r)
            allbookXpath = xpathHtml.xpath('//*[@id="search_book_list"]/*')
            for bookbox in allbookXpath:
                lanvage=bookbox[0].xpath('./span/text()')
                name=bookbox[0].xpath('./a/text()')[0]
                num=bookbox[0].xpath('./text()')
                num=' '.join(num)  #转化为字符串
                num=num.strip()    #删除两端空格并赋值给num
                href=whereurl+bookbox[0].xpath('./a/@href')[0]
                author=bookbox[1].xpath('./text()')[1]
                author=' '.join(author)
                author=author.strip()
                borrow=bookbox[1].xpath('./span/text()')[1]
                piblish=bookbox[1].xpath('./text()')[2]
                piblish=' '.join(piblish)
                piblish=piblish.strip()
                whereList=GetWhere(href)
                score=bookbox[1].xpath('./text()')[4]
                #print('第'+str(page)+'页'+name)
                j={'lanvage':lanvage,'name':name,'num':num,'author':author,'borrow':borrow,'publish':piblish,'whereList':whereList,'score':score}
                bookDetailList.append(j)
        return bookDetailList
    #'数学'
    allbookList=GetAllbook(value)
    # for b in allbookList:
    #     print(b['lanvage'],b['name'])
    print("value:",value)
    print("allbookList:",allbookList)
    return json.dumps(allbookList)
    #json.dumps(allbookList)
# findBook_func('微信')

# ----------------








r = requests.get('https://www.qidian.com/')
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, from_encoding='utf-8')


def free_func():
    countdown = soup.select('.time-limit-wrap #numero5 li')
    free = []
    for item in countdown:
        if item.attrs['class'][0] != 'time-box':
            info = {}
            if len(item.select('.book-img a img')) > 0:
                info['cover'] = item.select('.book-img a img')[0]['data-original']
            if len(item.select('.name')) > 0:
                info['url'] = item.select('.name')[0]['href']
                info['title'] = item.select('.name')[0].text
            free.append(info)
    return json.dumps(free)


def wrap_func():
    result = {}
    wrap = soup.select('#rank-list-row .rank-list')
    for item in wrap:
        if item['data-l2'] == "2":
            books_url = 'http:' + item.select('.wrap-title a')[0]['href']
            books_html = requests.get(books_url)
            books_soup = BeautifulSoup(books_html.text, from_encoding='utf-8')
            books = books_soup.select('.rank-body .book-img-text li')
            booklist = []
            num = 0
            for key in books:
                if num < 10:
                    info = {}
                    if len(key.select('.book-img-box a img')) > 0:
                        info['cover'] = key.select('.book-img-box a img')[0]['src']
                    if len(key.select('.book-mid-info h4 a')) > 0:
                        info['url'] = key.select('.book-mid-info h4 a')[0]['href']
                        info['title'] = key.select('.book-mid-info h4 a')[0].text
                    if len(key.select('.book-mid-info .author .name')) > 0:
                        info['actor'] = key.select('.book-mid-info .author .name')[0].text
                    booklist.append(info)
                num += 1
            index = 0
            wraplist = []
            wraplist1 = []
            for element in booklist:
                if index < 3:
                    wraplist1.append(element)
                else:
                    wraplist.append(element)
                index += 1
            result['wrapbox'] = wraplist
            result['wrap'] = wraplist1
    return json.dumps(result)


def week_func():
    wrap = soup.select('#rank-list-row .rank-list')
    for item in wrap:
        if item['data-l2'] == "4":
            books_url = 'http:' + item.select('.wrap-title a')[0]['href']
            books_html = requests.get(books_url)
            books_soup = BeautifulSoup(books_html.text, from_encoding='utf-8')
            books = books_soup.select('.rank-body .book-img-text li')
            booklist = []
            num = 0
            for key in books:
                if num < 10:
                    info = {}
                    if len(key.select('.book-img-box a img')) > 0:
                        info['cover'] = key.select('.book-img-box a img')[0]['src']
                    if len(key.select('.book-mid-info h4 a')) > 0:
                        info['url'] = key.select('.book-mid-info h4 a')[0]['href']
                        info['title'] = key.select('.book-mid-info h4 a')[0].text
                    if len(key.select('.book-mid-info .author .name')) > 0:
                        info['actor'] = key.select('.book-mid-info .author .name')[0].text
                    booklist.append(info)
                num += 1
    return json.dumps(booklist)


def writer_func():
    wrap = soup.select('#rank-list-row .rank-list')
    for item in wrap:
        if item['data-l2'] == "5":
            books_url = 'http:' + item.select('.wrap-title a')[0]['href']
            books_html = requests.get(books_url)
            books_soup = BeautifulSoup(books_html.text, from_encoding='utf-8')
            books = books_soup.select('.rank-body .book-img-text li')
            booklist = []
            num = 0
            for key in books:
                if num < 10:
                    info = {}
                    if len(key.select('.book-img-box a img')) > 0:
                        info['cover'] = key.select('.book-img-box a img')[0]['src']
                    if len(key.select('.book-mid-info h4 a')) > 0:
                        info['url'] = key.select('.book-mid-info h4 a')[0]['href']
                        info['title'] = key.select('.book-mid-info h4 a')[0].text
                    if len(key.select('.book-mid-info .author .name')) > 0:
                        info['actor'] = key.select('.book-mid-info .author .name')[0].text
                    booklist.append(info)
                num += 1
    return json.dumps(booklist)


def detailed_func(url):
    detailed = requests.get('http:' + url)
    detailed.encoding = 'utf-8'
    detailed_soup = BeautifulSoup(detailed.text, from_encoding='utf-8').select('.book-detail-wrap')[0]
    result = {}
    # 封面
    if len(detailed_soup.select('.book-information .book-img a img')) > 0:
        result['cover'] = detailed_soup.select('.book-information .book-img a img')[0]['src']
    # 标题
    if len(detailed_soup.select('.book-information .book-info h1 em')) > 0:
        result['title'] = detailed_soup.select('.book-information .book-info h1 em')[0].text
    # 作者
    if len(detailed_soup.select('.book-information .book-info h1 span a')) > 0:
        result['actor'] = detailed_soup.select('.book-information .book-info h1 span a')[0].text
    # 类型
    if len(detailed_soup.select('.book-information .book-info .tag a')) > 0:
        result['type'] = detailed_soup.select('.book-information .book-info .tag a')[0].text
    # 文案
    if len(detailed_soup.select('.book-information .book-info .intro')) > 0:
        result['slogan'] = detailed_soup.select('.book-information .book-info .intro')[0].text
    # 状态
    if len(detailed_soup.select('.book-information .book-info .tag span')) > 0:
        result['status'] = detailed_soup.select('.book-information .book-info .tag span')[0].text
    # 作品信息
    if len(detailed_soup.select('.book-info-detail .book-intro p')) > 0:
        result['des'] = detailed_soup.select('.book-info-detail .book-intro p')[0].text
    # 最近更新
    if len(detailed_soup.select('.book-info-detail .book-state .update')) > 0:
        result['updatetext'] = detailed_soup.select('.book-info-detail .book-state .update .detail .cf a')[0].text
        result['updateurl'] = detailed_soup.select('.book-info-detail .book-state .update .detail .cf a')[0]['href']
        result['updatetime'] = detailed_soup.select('.book-info-detail .book-state .update .detail .cf .time')[0].text
    return json.dumps(result)


def read_func(url, type):
    if type == 'try':
        detailed1 = requests.get('http:' + url)
        detailed1.encoding = 'utf-8'
        detailed1_soup = BeautifulSoup(detailed1.text, from_encoding='utf-8').select('.book-detail-wrap')[0]
        # 试读文章
        if len(detailed1_soup.select('.book-information .book-info p .J-getJumpUrl')) > 0:
            read_url = detailed1_soup.select('.book-information .book-info p .J-getJumpUrl')[0]['href']
    else:
        read_url = url
    read = requests.get('http:' + read_url)
    read.encoding = 'utf-8'
    read_soup = BeautifulSoup(read.text, from_encoding='utf-8')
    result = {}
    if len(read_soup.select('.wrap .read-main-wrap #j_chapterBox .text-wrap .main-text-wrap')) > 0:
        # 标题
        result['title'] = read_soup.select('.read-main-wrap #j_chapterBox .text-wrap .main-text-wrap .text-head h3')[
            0].text
        # 内容
        result['content'] = read_soup.select('.read-main-wrap #j_chapterBox .text-wrap .main-text-wrap .read-content')[
            0].text
    if len(read_soup.select('.read-main-wrap .chapter-control')) > 0:
        # 下一章
        result['next'] = read_soup.select('.read-main-wrap .chapter-control #j_chapterNext')[0]['href']
        # 上一章
        result['prev'] = read_soup.select('.read-main-wrap .chapter-control #j_chapterPrev')[0]['href']
    if len(read_soup.select('.read-main-wrap .main-text-wrap .vip-limit-wrap')) > 0:
        result['vip'] = False
    else:
        result['vip'] = True
    return json.dumps(result)


def list_func(url):
    detailed2 = requests.get('http:' + url)
    detailed2.encoding = 'utf-8'
    list_soup = BeautifulSoup(detailed2.text, from_encoding='utf-8').select('.book-detail-wrap')[0]
    result = []
    if len(list_soup.select('.catalog-content-wrap .volume-wrap')) > 0:
        volumelist = list_soup.select('.catalog-content-wrap .volume-wrap')
        for item in volumelist:
            volume = {}
            if len(item.select('.volume h3')) > 0:
                volume['title'] = item.select('.volume h3')[0].text
            if len(item.select('.volume ul li')) > 0:
                content = []
                for key in item.select('.volume ul li'):
                    content_info = {}
                    content_info['title'] = key.select('a')[0].text
                    content_info['url'] = key.select('a')[0]['href']
                    content_info['time'] = key.select('a')[0]['title']
                    content.append(content_info)
                volume['content'] = content
            result.append(volume)
    return json.dumps(result)


def groom_func():
    groom = requests.get('http://www.qidian.com/search?kw=')
    groom.encoding = 'utf-8'
    groom_soup = BeautifulSoup(groom.text, from_encoding='utf-8')
    data = []
    if len(groom_soup.select('#result-list .book-img-text li')) > 0:
        resultlist = groom_soup.select('#result-list .book-img-text li')
        for item in resultlist:
            result = {}
            if len(item.select('.book-img-box a img')) > 0:
                result['cover'] = item.select('.book-img-box a img')[0]['src']
            if len(item.select('.book-mid-info h4 a')) > 0:
                result['url'] = item.select('.book-mid-info h4 a')[0]['href']
                result['title'] = item.select('.book-mid-info h4 a')[0].text
            if len(item.select('.book-mid-info .author .name')) > 0:
                result['actor'] = item.select('.book-mid-info .author .name')[0].text
            if len(item.select('.book-mid-info .author a')) > 1:
                result['type'] = item.select('.book-mid-info .author a')[1].text
            if len(item.select('.book-mid-info .author span')) > 0:
                result['status'] = item.select('.book-mid-info .author span')[0].text
            if len(item.select('.book-mid-info .intro')) > 0:
                result['des'] = item.select('.book-mid-info .intro')[0].text
            data.append(result)
    return json.dumps(data)


def search_func(value):
    search = requests.get('http://www.qidian.com/search?kw=' + value)
    search.encoding = 'utf-8'
    search_soup = BeautifulSoup(search.text, from_encoding='utf-8')
    if len(search_soup.select('#result-list .book-img-text li')) > 0:
        data = []
        resultlist = search_soup.select('#result-list .book-img-text li')
        for item in resultlist:
            result = {}
            if len(item.select('.book-img-box a img')) > 0:
                result['cover'] = item.select('.book-img-box a img')[0]['src']
            if len(item.select('.book-mid-info h4 a')) > 0:
                result['url'] = item.select('.book-mid-info h4 a')[0]['href']
                result['title'] = item.select('.book-mid-info h4 a')[0].text
            if len(item.select('.book-mid-info .author .name')) > 0:
                result['actor'] = item.select('.book-mid-info .author .name')[0].text
            if len(item.select('.book-mid-info .author a')) > 1:
                result['type'] = item.select('.book-mid-info .author a')[1].text
            if len(item.select('.book-mid-info .author span')) > 0:
                result['status'] = item.select('.book-mid-info .author span')[0].text
            if len(item.select('.book-mid-info .intro')) > 0:
                result['des'] = item.select('.book-mid-info .intro')[0].text
            data.append(result)
    return json.dumps(data)
