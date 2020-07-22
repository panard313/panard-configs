#!user/bin/python
# -*- coding:utf-8 -*-
# author: jianhua.he@tcl.com

import sys
import os
import datetime
import time
import re
import platform
import getopt
import threading
from subprocess import Popen, PIPE, call
import urllib
import urllib2
import logging
import requests
import socket


global number_download_apks
number_download_apks = 100

global download_apks_n_now
download_apks_n_now = 0

global apks_save_path
#apks_save_path = "d:\\downloadtop100apks\\"
apks_save_path = "./"




class downloadBaiduList:
    def log(self, strs):
        logging.basicConfig(level=logging.DEBUG,
                            # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            # datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='appiinfo.log',
                            filemode='w')


        logging.info(strs)


    def baiduStoreAppInfo(self, url):
        print(url)
        print ""
        print ""
        
        try:
            response = urllib2.urlopen(url)
            content = response.read().decode('utf-8')
            response.close()
        except urllib2 as e:
            print "had issue:", e
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            return
        
        pattern_str = 'data-pos=.*? data_type=.*? data_url=.*? data_name=.*? data_detail_type=.*? data_package=.*? data_versionname=.*? data_icon=.*? data_from=.*? data_size=.*?>'
        pattern = re.compile(pattern_str, re.S)
        name_items = re.findall(pattern, content)
        print(name_items)
        count_item = 0
        for item in name_items:
            print count_item," app info:", item
            
            #位置
            match_result = re.match('data-pos=\"(.*?)\"', item)
            if match_result:
                print match_result.group(1)
                datapos = match_result.group(1)
            else:
                print "had no match data pos", pattern_str
                continue
                
            #下载地址
            match_result = re.search('data_url=\"(.*?)\"', item)
            if match_result:
                print match_result.group(1)
                dataurl = match_result.group(1)
            else:
                print "had no match data url", pattern_str
                continue
                
            #中文名字
            match_result = re.search('data_name=\"(.*?)\"', item)
            if match_result:
                print match_result.group(1)
                dataname = match_result.group(1)
            else:
                print "had no match data name", pattern_str
                continue
                
            #包名
            match_result = re.search('data_package=\"(.*?)\"', item)
            if match_result:
                print match_result.group(1)
                datapackage = match_result.group(1)
            else:
                print "had no match data package", pattern_str
                continue
            
            #版本号
            match_result = re.search('data_versionname=\"(.*?)\"', item)
            if match_result:
                print match_result.group(1)
                dataversion = match_result.group(1)
            else:
                print "had no match data version", pattern_str
                continue
            
            #文件大小
            match_result = re.search('data_size=\"(.*?)\"', item)
            if match_result:
                print match_result.group(1)
                datasize = match_result.group(1)
            else:
                print "had no match data size", pattern_str
                continue
                
            global apks_save_path
            global download_apks_n_now
            global number_download_apks
            if not os.path.exists(apks_save_path):
                os.mkdir(apks_save_path)
            save_filename = apks_save_path + str(download_apks_n_now) + "" + dataname +"" + datapackage + "_" +dataversion + ".apk"
            print "will save to :", save_filename
            isSuccess = self.auto_down(dataurl, save_filename)
            
            if isSuccess:
                count_item = count_item + 1
                download_apks_n_now = download_apks_n_now + 1
            time.sleep(1)
            if download_apks_n_now >= number_download_apks:
                print "already Download full apks"
                break
            
            
    # 解决urlretrieve下载文件不完全的问题且避免下载时长过长陷入死循环
    def auto_down(self, url, filename):
        try:
            print("now downloading ......")
            print(url)
           # dicts = appurl.download_apk(url)
            urllib.urlretrieve(url, filename, self.Schedule)
            '''headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) '
                          'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Connection': 'keep-alive', }
            file = requests.get(url, headers=headers, timeout=30)
            with open(filename, 'wb') as apk:
                apk.write(file.content)'''
            print(download_apks_n_now, " Download this apk DONE!!")
            return True
        except Exception as e:
            count = 1
            while count <= 15:
                try:
                    print("正在下载应用 count: ")
                    #dicts = appurl.download_apk(url)
                    urllib.urlretrieve(url, filename, self.Schedule)
                    print("下载完成 count")
                    return True
                    break
                except socket.timeout:
                    err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                    print(err_info)
                    count += 1
                except Exception as e:
                    print("Exception" + Exception + e)
                    continue
            if count > 15:
                if(os.path.exists(filename)):
                    os.remove(filename)
                print(download_apks_n_now," Download failed...")
                return False
        time.sleep(1)
        return False
        
    def Schedule(self,a,b,c):
       '''
       a:已经下载的数据块
       b:数据库块的大小
       c:远程文件的大小
       '''
       per = 100.0 * a * b / c
       if per>100:
           per = 100
           print(download_apks_n_now, ' success!')
           time.sleep(2)
       print('%.2f%%' % per)
       
       
       
       

def check_inpute_parameter(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hvn:', ['number='])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print "usage:"
            print "-h, (--help) : "
            print "-v, (--version): tool version"
            print "-n, (--number) : the download app top N number"
            sys.exit(1)
        elif opt in ('-v', '--version'):
            print "version 2.0"
            sys.exit(0)
        elif opt in ('-n', '--number'):
            if arg != "" and len(arg) >= 1:
                global number_download_apks
                number_download_apks = int(arg)
                print "you set download app unmber is",number_download_apks 
        else:
            print 'unhandled option'
            sys.exit(3)
            
            
if __name__ == "__main__":
    check_inpute_parameter(sys.argv)
    d = downloadBaiduList()
    #url = 'http://shouji.baidu.com/rank/top/software/'+ "list_" + str(3) + ".html"
    #d.baiduStoreAppInfo(url)
    for i in range(1, 11):
        if download_apks_n_now <= number_download_apks:
            url = 'http://shouji.baidu.com/rank/top/software/'+ "list_" + str(i) + ".html"
            d.baiduStoreAppInfo(url)
        else:
            print ""
            print ""
            print ""
            print download_apks_n_now, " apks, Download apk DONE!!!"
            print "to check apks at folder: ", apks_save_path
            break
            
            
            