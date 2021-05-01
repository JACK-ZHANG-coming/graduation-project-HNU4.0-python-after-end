import json
import re
from retrying import retry

import requests
from control.fateadm_api import TestFunc
from lxml import etree

flag1=0
class Spider:

    def __init__(self, username, pwd):
        print("username:", username, "pwd:", pwd)
        self.username = username
        self.pwd = pwd
        self.captchaurl = "http://ecard.hytc.edu.cn/AuthCode.aspx?"
        self.loginurl = "http://ecard.hytc.edu.cn/default.aspx"
        self.history_url = "http://ecard.hytc.edu.cn/Cardholder/Queryhistory.aspx"
        self.s = requests.session()

    def getcaptcha(self):
        headers = {
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "ecard.hytc.edu.cn",
            "Pragma": "no-cache",
            "Referer": "http://ecard.hytc.edu.cn/default.aspx",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }
        response = self.s.get(self.captchaurl, headers=headers)
        with open('test.jpg', 'wb') as f:
            f.write(response.content)
        res = TestFunc(response.content)
        return res
    @retry(stop_max_attempt_number=5)
    def login(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "835",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "ecard.hytc.edu.cn",
            "Origin": "http://ecard.hytc.edu.cn",
            "Pragma": "no-cache",
            "Referer": "http://ecard.hytc.edu.cn/default.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }
        res = self.getcaptcha()
        print("验证码识别结果：", res)
        data = "__LASTFOCUS=&__EVENTTARGET=UserLogin%24ImageButton1&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTc0MDQ4ODc3Nw9kFgICAQ9kFhICAw8WAh4HVmlzaWJsZWhkAgUPFgIfAGhkAgcPFgIfAGhkAgkPPCsACQEADxYEHghEYXRhS2V5cxYAHgtfIUl0ZW1Db3VudGZkZAIODzwrAAkBAA8WBB8BFgAfAmZkZAIQDzwrAAkBAA8WBB8BFgAfAmZkZAISDzwrAAkBAA8WBB8BFgAfAmZkZAIUDzwrAAkBAA8WBB8BFgAfAmZkZAIWDzwrAAkBAA8WBB8BFgAfAmZkZGQwoSnp5LzkYCr5ET50lv4hq5VTyOPH7j7FKlm3Ns3Ttw%3D%3D&__VIEWSTATEGENERATOR=CA0B0334&__EVENTVALIDATION=%2FwEdAAkRR7P5YqlhtPBDr9LsW9TZohjo8sIky4Xs%2BCUBsum%2BnL6pRh%2FvC3eYiguVzFy%2FtEYvT53BE9ULYNj8jfQiCQeC35ZbbeGbJddowj1pY7sNivrI0G85IvfKPX4CghIMZ1NJ4PbCb80KUDHFYYKXgFT9PjMyUg6NAZP4%2BvrIPkQUuFOdcKl43UA3HbIoQpEPelg15C1xJZFr7yUnq13Hgg6jEvssGBy5%2Bz9cazf4WQxSqg%3D%3D&UserLogin%3AtxtUser={}&UserLogin%3AtxtPwd={}&UserLogin%3AddlPerson=%BF%A8%BB%A7&UserLogin%3AtxtSure={}".format(
            self.username, self.pwd, res)
        response = self.s.post(self.loginurl, headers=headers, data=data)
        if '退出登录' in response.text:
            print("登录成功")
            self.index_html = response.text
        else:
            print('登录失败')
            print('log in error')
            flag1=1
            # 重试
            # raise Exception("log in error")

    def get_balance(self):
        balance = re.findall('<span id="lblOne0">(.*?)</span>', self.index_html)
        Acc = re.findall('<span id="lblInAcc">(.*?)</span>', self.index_html)
        Percode = re.findall('<span id="lblInPercode">(.*?)</span>', self.index_html)
        Name = re.findall('<span id="lblInName">(.*?)</span>', self.index_html)
        Sex = re.findall('<span id="lblInSex">(.*?)</span>', self.index_html)
        Dep = re.findall('<span id="lblInDep">(.*?)</span>', self.index_html)
        print(balance, Acc, Percode, Name, Sex, Dep)
        j={"balance":balance,"Acc":Acc,"Percode":Percode,"Name":Name,"Sex":Sex,"Dep":Dep}
        return j

    def gethistory(self, startdate, enddate):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "976",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "ecard.hytc.edu.cn",
            "Origin": "http://ecard.hytc.edu.cn",
            "Pragma": "no-cache",
            "Referer": "http://ecard.hytc.edu.cn/Cardholder/Queryhistory.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }
        data = "__EVENTTARGET=ImageButton1&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTI1NTA5NTE5OQ8WCh4NZEJlZ2luUmVjVGltZQUTMjAyMC0wMy0wMSAwMDowMDowMB4LZEVuZFJlY1RpbWUFEzIwMjAtMDMtMDggMjM6NTk6NTkeClBhZ2VzQ291bnRmHglQYWdlSW5kZXhmHglKdW1wUGFnZXMCARYCAgEPZBYWAgEPZBYCAgEPDxYCHgRUZXh0BQblvKDlvLpkZAIRDzwrAAsBAA8WCB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQCAR4JUGFnZUNvdW50AgEeFV8hRGF0YVNvdXJjZUl0ZW1Db3VudAIBZBYCZg9kFgICAQ9kFhZmDw8WAh8FBQg1NDMxNjAzNmRkAgEPDxYCHwUFCTIwMTcxNDQ5NGRkAgIPDxYCHwUFA0NQVWRkAgMPDxYCHwUFDOWNoeaIt%2BaUueWvhmRkAgQPDxYCHwUFBiZuYnNwO2RkAgUPDxYCHwUFDOW%2BruS%2FoeaUr%2BS7mGRkAgYPDxYCHwUFATBkZAIHDw8WAh8FBQQwLjAwZGQCCA8PFgIfBQUQMjAyMC0wMy0wMSAxNTozNWRkAgkPDxYCHwUFCeS4u%2BmSseWMhWRkAgoPDxYCHwUFBjY3OC40OGRkAhUPDxYCHwUFATFkZAIZDw8WAh8FBQExZGQCHQ8PFgIfBQUBMWRkAh8PDxYCHgdFbmFibGVkaGRkAiEPDxYCHwpoZGQCIw8PFgIfCmhkZAIlDw8WAh8KaGRkAikPDxYEHwUFATEfCmhkZAItDw8WAh8KaGRkZO8pSDpCxZxnu8BHMIzqfpKOTuXWwcSpThEJSLjHcAsj&__VIEWSTATEGENERATOR=A64C3996&ECalendar_date={}&ECalendar_date2={}".format(
            startdate, enddate)
        response = self.s.post(self.history_url, headers=headers, data=data)
        html = etree.HTML(response.text)
        allpage = html.xpath('//*[@id="lbRecordCount"]/text()')
        print(allpage)
        history_list = html.xpath('//*[@id="dgShow"]/tr')
        result = []
        for i in history_list[1:]:
            print(i.xpath('td/text()'))
            result.append(i.xpath('td/text()'))
        for page in range(1, int(int(allpage[0])/12)+1):
            data = '__EVENTTARGET=Nextpage&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTI1NTA5NTE5OQ8WCh4NZEJlZ2luUmVjVGltZQUTMjAxOS0xMC0wOCAwMDowMDowMB4LZEVuZFJlY1RpbWUFEzIwMjAtMDMtMDggMjM6NTk6NTkeClBhZ2VzQ291bnQCJB4JUGFnZUluZGV4Zh4JSnVtcFBhZ2VzAiUWAgIBD2QWHAIBD2QWAgIBDw8WAh4EVGV4dAUG5byg5by6ZGQCBw8PZBYCHgVjbGFzcwUSYWN0aXZlIGNob29zZS10aW1lZAIJDw9kFgIfBgULY2hvb3NlLXRpbWVkAgsPD2QWAh8GBQtjaG9vc2UtdGltZWQCEQ88KwALAQAPFggeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50AgweCVBhZ2VDb3VudAIBHhVfIURhdGFTb3VyY2VJdGVtQ291bnQCDGQWAmYPZBYYAgEPZBYWZg8PFgIfBQUINDczNzgyODVkZAIBDw8WAh8FBQkyMDE3MTQ0OTRkZAICDw8WAh8FBQ5NMUNQVea3t%2BWQiOWNoWRkAgMPDxYCHwUFDOWNoeaIt%2BWtmOasvmRkAgQPDxYCHwUFBiZuYnNwO2RkAgUPDxYCHwUFDOW%2BruS%2FoeaUr%2BS7mGRkAgYPDxYCHwUFATBkZAIHDw8WAh8FBQUzMC4wMGRkAggPDxYCHwUFEDIwMTktMTAtMDggMTA6NDdkZAIJDw8WAh8FBQnkuLvpkrHljIVkZAIKDw8WAh8FBQU0Ni41NGRkAgIPZBYWZg8PFgIfBQUINDczNzg4MzVkZAIBDw8WAh8FBQkyMDE3MTQ0OTRkZAICDw8WAh8FBQ5NMUNQVea3t%2BWQiOWNoWRkAgMPDxYCHwUFDOihpeWKqeWciOWtmGRkAgQPDxYCHwUFKOWNl%2BiLkeS6jOalvOmlrumjn%2BS%2Bm%2BW6lOeCue%2B8iDLlj7fmpbzvvIlkZAIFDw8WAh8FBQrlraYy5raI6LS5ZGQCBg8PFgIfBQUBM2RkAgcPDxYCHwUFBDAuMDBkZAIIDw8WAh8FBRAyMDE5LTEwLTA4IDEwOjU2ZGQCCQ8PFgIfBQUJ5Li76ZKx5YyFZGQCCg8PFgIfBQUFNDYuNTRkZAIDD2QWFmYPDxYCHwUFCDQ3Mzc4ODM2ZGQCAQ8PFgIfBQUJMjAxNzE0NDk0ZGQCAg8PFgIfBQUOTTFDUFXmt7flkIjljaFkZAIDDw8WAh8FBQzllYbliqHmlLbotLlkZAIEDw8WAh8FBSjljZfoi5Hkuozmpbzppa7po5%2FkvpvlupTngrnvvIgy5Y%2B35qW877yJZGQCBQ8PFgIfBQUK5a2mMua2iOi0uWRkAgYPDxYCHwUFATNkZAIHDw8WAh8FBQUtOC40MGRkAggPDxYCHwUFEDIwMTktMTAtMDggMTA6NTZkZAIJDw8WAh8FBQnkuLvpkrHljIVkZAIKDw8WAh8FBQUzOC4xNGRkAgQPZBYWZg8PFgIfBQUINDczNzg4NDRkZAIBDw8WAh8FBQkyMDE3MTQ0OTRkZAICDw8WAh8FBQ5NMUNQVea3t%2BWQiOWNoWRkAgMPDxYCHwUFDOWVhuWKoeaUtui0uWRkAgQPDxYCHwUFKOWNl%2BiLkeS6jOalvOmlrumjn%2BS%2Bm%2BW6lOeCue%2B8iDLlj7fmpbzvvIlkZAIFDw8WAh8FBQrlraYy5raI6LS5ZGQCBg8PFgIfBQUBM2RkAgcPDxYCHwUFBS04LjQwZGQCCA8PFgIfBQUQMjAxOS0xMC0wOCAxMDo1NmRkAgkPDxYCHwUFCeS4u%2BmSseWMhWRkAgoPDxYCHwUFBTI5Ljc0ZGQCBQ9kFhZmDw8WAh8FBQg0NzQwNjYyM2RkAgEPDxYCHwUFCTIwMTcxNDQ5NGRkAgIPDxYCHwUFDk0xQ1BV5re35ZCI5Y2hZGQCAw8PFgIfBQUM5ZWG5Yqh5pS26LS5ZGQCBA8PFgIfBQUM5YyX6IuR5LiA5qW8ZGQCBQ8PFgIfBQUM5YyX6IuR6aOf5aCCZGQCBg8PFgIfBQUCMzZkZAIHDw8WAh8FBQYtMTAuMDBkZAIIDw8WAh8FBRAyMDE5LTEwLTA4IDE3OjEzZGQCCQ8PFgIfBQUJ5Li76ZKx5YyFZGQCCg8PFgIfBQUFMTkuNzRkZAIGD2QWFmYPDxYCHwUFCDQ3NDEyNTU2ZGQCAQ8PFgIfBQUJMjAxNzE0NDk0ZGQCAg8PFgIfBQUOTTFDUFXmt7flkIjljaFkZAIDDw8WAh8FBQzllYbliqHmlLbotLlkZAIEDw8WAh8FBQU1I%2BW8gGRkAgUPDxYCHwUFCuWtpjXlvIDmsLRkZAIGDw8WAh8FBQE0ZGQCBw8PFgIfBQUFLTAuMzBkZAIIDw8WAh8FBRAyMDE5LTEwLTA4IDE3OjQxZGQCCQ8PFgIfBQUJ5Li76ZKx5YyFZGQCCg8PFgIfBQUFMTkuNDRkZAIHD2QWFmYPDxYCHwUFCDQ3NDEyNTY2ZGQCAQ8PFgIfBQUJMjAxNzE0NDk0ZGQCAg8PFgIfBQUOTTFDUFXmt7flkIjljaFkZAIDDw8WAh8FBQzllYbliqHmlLbotLlkZAIEDw8WAh8FBQU1I%2BW8gGRkAgUPDxYCHwUFCuWtpjXlvIDmsLRkZAIGDw8WAh8FBQE0ZGQCBw8PFgIfBQUFLTAuMDJkZAIIDw8WAh8FBRAyMDE5LTEwLTA4IDE3OjQxZGQCCQ8PFgIfBQUJ5Li76ZKx5YyFZGQCCg8PFgIfBQUFMTkuNDJkZAIID2QWFmYPDxYCHwUFCDQ3NDEyNTcxZGQCAQ8PFgIfBQUJMjAxNzE0NDk0ZGQCAg8PFgIfBQUOTTFDUFXmt7flkIjljaFkZAIDDw8WAh8FBQzllYbliqHmlLbotLlkZAIEDw8WAh8FBQU1I%2BW8gGRkAgUPDxYCHwUFCuWtpjXlvIDmsLRkZAIGDw8WAh8FBQE0ZGQCBw8PFgIfBQUFLTAuMDJkZAIIDw8WAh8FBRAyMDE5LTEwLTA4IDE3OjQxZGQCCQ8PFgIfBQUJ5Li76ZKx5YyFZGQCCg8PFgIfBQUFMTkuNDBkZAIJD2QWFmYPDxYCHwUFCDQ3NDYzOTg2ZGQCAQ8PFgIfBQUJMjAxNzE0NDk0ZGQCAg8PFgIfBQUOTTFDUFXmt7flkIjljaFkZAIDDw8WAh8FBQzllYbliqHmlLbotLlkZAIEDw8WAh8FBRjlrabkupTljZfkuIDmiZPlrZflpI3ljbBkZAIFDw8WAh8FBQrlraY15raI6LS5ZGQCBg8PFgIfBQUBNmRkAgcPDxYCHwUFBS0xLjAwZGQCCA8PFgIfBQUQMjAxOS0xMC0wOSAwODoyMGRkAgkPDxYCHwUFCeS4u%2BmSseWMhWRkAgoPDxYCHwUFBTE4LjQwZGQCCg9kFhZmDw8WAh8FBQg0NzQ2NDA4MmRkAgEPDxYCHwUFCTIwMTcxNDQ5NGRkAgIPDxYCHwUFDk0xQ1BV5re35ZCI5Y2hZGQCAw8PFgIfBQUM5ZWG5Yqh5pS26LS5ZGQCBA8PFgIfBQUY5a2m5LqU5Y2X5LqM55m%2B6LSn5ZWG5bqXZGQCBQ8PFgIfBQUK5a2mNea2iOi0uWRkAgYPDxYCHwUFATNkZAIHDw8WAh8FBQUtOS4wMGRkAggPDxYCHwUFEDIwMTktMTAtMDkgMDg6MjBkZAIJDw8WAh8FBQnkuLvpkrHljIVkZAIKDw8WAh8FBQQ5LjQwZGQCCw9kFhZmDw8WAh8FBQg0NzQ3MjQyMmRkAgEPDxYCHwUFCTIwMTcxNDQ5NGRkAgIPDxYCHwUFDk0xQ1BV5re35ZCI5Y2hZGQCAw8PFgIfBQUM5ZWG5Yqh5pS26LS5ZGQCBA8PFgIfBQUM5Y2X6IuR5LiA5qW8ZGQCBQ8PFgIfBQUM5Y2X6IuR6aOf5aCCZGQCBg8PFgIfBQUCMjZkZAIHDw8WAh8FBQUtNy44MGRkAggPDxYCHwUFEDIwMTktMTAtMDkgMTE6MzdkZAIJDw8WAh8FBQnkuLvpkrHljIVkZAIKDw8WAh8FBQQxLjYwZGQCDA9kFhZmDw8WAh8FBQg0NzQ4NDk4M2RkAgEPDxYCHwUFCTIwMTcxNDQ5NGRkAgIPDxYCHwUFDk0xQ1BV5re35ZCI5Y2hZGQCAw8PFgIfBQUM5ZWG5Yqh5pS26LS5ZGQCBA8PFgIfBQUFNSPlvIBkZAIFDw8WAh8FBQrlraY15byA5rC0ZGQCBg8PFgIfBQUBNGRkAgcPDxYCHwUFBS0wLjMwZGQCCA8PFgIfBQUQMjAxOS0xMC0wOSAxMzo1NWRkAgkPDxYCHwUFCeS4u%2BmSseWMhWRkAgoPDxYCHwUFBDEuMzBkZAIVDw8WAh8FBQExZGQCGQ8PFgIfBQUCMzdkZAIdDw8WAh8FBQM0MzNkZAIfDw8WAh4HRW5hYmxlZGhkZAIhDw8WAh8LaGRkAiMPDxYCHwtnZGQCJQ8PFgIfC2dkZAIpDw8WAh8LZ2RkAi0PDxYCHwtnZGRk2TK5odbitKSpBmB13e8wKM3zV%2FtSjsynbjZYp%2B58m60%3D&__VIEWSTATEGENERATOR=A64C3996&ECalendar_date={}&ECalendar_date2={}&GotoPage={}'.format(
                startdate, enddate, page)
            response = self.s.post(self.history_url, headers=headers, data=data)
            html = etree.HTML(response.text)
            history_list = html.xpath('//*[@id="dgShow"]/tr')
            for i in history_list[1:]:
                print(i.xpath('td/text()'))
                result.append(i.xpath('td/text()'))
        return result


# if __name__ == '__main__':
# 小程序传输进来的格式
# 学号密码
# x="2116130039130871"
# 查询起止时间
# y="2116130039130871&2019-10-1|2019-10-9"
# bug---页面访问多次，网站无法访问，不知是否是反爬虫

# 余额首页
def gotoHome(x):
    print("x:",x)
    studentID=x[0:10]
    studentPassword=x[10:] #截取规则、第一个位置是从0开始，第二个位置截取到那位是从1开始
    print("studentID:",studentID,"studentPassword:",studentPassword,"学号长度",len(studentID))
    # s = Spider("2116130039", "130871")
    s = Spider(studentID, studentPassword)
    s.login()
    a=s.get_balance()
    if flag1!=0:
        b="passwordError"
        return json.dumps(b)
    else:
        print("a:",a)
        return json.dumps(a)
    # s.gethistory("2019-10-1", "2019-10-9")

# 查询消费记录
def gotoBalance(y):
    firstdate=""
    lastdate=""
    user=""
    flag=0
    # 将时间字符串分隔
    for i in range(0, len(y)):
        if y[i]=='z':
            flag=flag+1
            print("flag:",flag)
        elif flag==0 :
            user=user+y[i]
        elif flag==1:
            firstdate=firstdate+y[i]
        else:
            lastdate=lastdate+y[i]
    print("user:",user,"firstdate:",firstdate,"lastdate:",lastdate)
    studentID = user[0:10]
    studentPassword = user[10:] #截取到最后一位
    s = Spider(studentID, studentPassword)
    s.login()
    # s.get_balance()
    a=s.gethistory(firstdate, lastdate)
    print("a:",a)
    return json.dumps(a)
# gotoHome(x)
# print(y)
# gotoBalance(y)


# s = Spider("2116130039", "130871")
# s.login()
# s.get_balance()