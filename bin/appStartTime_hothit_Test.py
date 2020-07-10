#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
'''
@author: jianhua.he@tcl.com, kevinjh443@163.com
@date: 2016-03-30
       2019-08-08 add hot hit test
'''
import sys
import os
import datetime
import time
import re
import platform
import getopt
import threading
from subprocess import Popen, PIPE, call


class SelectDevice():
    """
    select device id lib class
    """
    def select_device(self):
        device_list = self.__get_device_list()
        if device_list:
            device_num = 0
            for device in device_list:
                print "%d -- %s" % (device_num, device)
                device_num += 1
        else:
            print "Cannot find devices!!!"
            sys.exit(1)
        print ""
        device_index = input("Please select one device: ")
        return device_list[device_index]
    
    def __get_device_list(self):
        dev_list = []
        call('adb start-server', shell=True)
        return_value = Popen('adb devices', shell=True, stdout=PIPE).stdout.readlines()
        for line in return_value:
            m_dev_id = re.match(r'(\w+)(?=\t)', line)
            if m_dev_id:
                dev_id = m_dev_id.group()
                dev_list.append(dev_id)
        return dev_list

def initHtml(htmlfile):
    '''write basic html file'''
    initCode = """<html><head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title>app start report</title>
    <style type="text/css"> 
    .table 
    { 
    width: 80%; 
    padding: 0; 
    margin: 0; 
    } 
    th { 
    font: bold 12px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif; 
    color: #4f6b72; 
    border-right: 1px solid #C1DAD7; 
    border-bottom: 1px solid #C1DAD7; 
    border-top: 1px solid #C1DAD7; 
    letter-spacing: 2px; 
    text-transform: uppercase; 
    text-align: left; 
    padding: 6px 6px 6px 12px; 
    background: #CAE8EA no-repeat; 
    } 
    .tdimpotant {
    background: #77DDFF;
    font-weight:bold;
    }
    td { 
    border-right: 1px solid #C1DAD7; 
    border-bottom: 1px solid #C1DAD7; 
    background: #fff; 
    font-size:14px; 
    padding: 6px 6px 6px 12px; 
    color: #4f6b72; 
    } 
    td.alt { 
    background: #F5FAFA; 
    color: #797268; 
    } 
    th.spec,td.spec { 
    border-left: 1px solid #C1DAD7; 
    } 
    /*---------for IE 5.x bug*/ 
    html>body td{ font-size:14px;} 
    tr.select th,tr.select td 
    { 
    background-color:#CAE8EA; 
    color: #797268; 
    } 
    </style>
    <head><body>
    <center>
    </br>
    <table class="table" border=1 cellspacing='0' cellpadding='0'>
    <tr> 
    <th class="spec">apk name</th> 
    <th>item</th> 
    <th>launch 1 (s)</th> 
    <th>launch 2 (s)</th> 
    <th>launch 3 (s)</th> 
    <th>launch 4 (s)</th> 
    <th>launch 5 (s)</th> 
    <th>launch 6 (s)</th> 
    <th>AVE launch (s)</th> 
    </tr> 
    """
    htmlfile.write(initCode)


def clear_recent():
    cmd_line1 = "adb -s " + static_usage.device_id + " shell input keyevent 4"#back key
    #cmd_line2 = "adb -s " + static_usage.device_id + " shell input tap 545 1660"
    #cmd_line2 = "adb -s " + static_usage.device_id + " shell input tap 690 2444"
    os.popen(cmd_line1)
    time.sleep(1)
    #os.popen(cmd_line2)
    #time.sleep(1)

def back_exit_app():
    cmd_line1 = "adb -s " + static_usage.device_id + " shell input keyevent 4"#back key
    os.popen(cmd_line1)
    time.sleep(0.05)
    os.popen(cmd_line1)
    time.sleep(2)

def home_exit_app():
    cmd_line1 = "adb -s " + static_usage.device_id + " shell input keyevent 3"#home key
    os.popen(cmd_line1)
    time.sleep(0.05)
    os.popen(cmd_line1)
    time.sleep(2)

def kill_this_app(app):
    appinfo = app.split("/")
    pakname = appinfo[0].strip()
    #print("get package name:"+pakname)
    if isWindowsSystem():
        result = Popen("adb -s " + static_usage.device_id + " shell ps -A | findstr "+pakname, shell=True, stdout=PIPE).stdout.readlines()
    else:
        result = Popen("adb -s " + static_usage.device_id + " shell ps -A | grep "+pakname, shell=True, stdout=PIPE).stdout.readlines()
    
    if 0!=len(result):
        resultinfo = result[0].split(' ')
        #print("split result,(get PID, if cannot kill process, please attention, contacts with jianhua.he@tcl Ext.66051 to change python script):")
        #print(resultinfo)
        #print("will kill this PID:"+resultinfo[5].strip())
        #call("adb -s " + static_usage.device_id + " shell kill "+resultinfo[5].strip(), shell=True)
        print("force-stop package :"+pakname)
        call("adb -s " + static_usage.device_id + " shell am force-stop "+pakname, shell=True)
        time.sleep(4)
    else:
        print("have not started yet!")

def isWindowsSystem():
    return 'Windows' in platform.system()

def get_apps(app_choice_file):
    app_list = []
    file = open(app_choice_file, "r")
    lists = file.readlines()
    file.close()
    for i in lists:
        if i.strip() == "":
            continue
        if ": " in i:
            appinfo = i.split(": ")
            app_list.append(appinfo[1].strip())
        else:
            app_list.append(i.strip())
    app_dic = {}.fromkeys(app_list)
    return app_dic


class ThreadStartApp(threading.Thread):
    """
    the sub thread for start app
    """
    def __init__(self, app, device_id, htmlfile = None):
        """
        app info, device id num, html file
        """
        threading.Thread.__init__(self)
        self.app = app
        self.device_id = device_id
        self.htmlfile = htmlfile
        self.start_times = {}.fromkeys(("ThisTime", "TotalTime", "WaitTime"))
        
    def get_start_times(self):
        return self.start_times
    
    def run(self):
        cmd_line = "adb -s " + self.device_id + " shell am start -W -n " + self.app#QCOM MTK same command
        print cmd_line
        if self.htmlfile != None:
            self.htmlfile.write(cmd_line+" </br>\n")
        result = os.popen(cmd_line).readlines()
        for line in result:
            if "ThisTime:" in line:
                _time = re.search(r'\s\d+', line)
                print _time
                self.start_times["ThisTime"] = _time.group().strip()
            if "TotalTime:" in line:
                _time = re.search(r'\s\d+', line)
                self.start_times["TotalTime"] = _time.group().strip()
            if "WaitTime:" in line:
                _time = re.search(r'\s\d+', line)
                self.start_times["WaitTime"] = _time.group().strip()
        
def get_times(app):
    start_times = {}.fromkeys(("ThisTime", "TotalTime", "WaitTime"))
    cmd_line = "adb -s " + static_usage.device_id + " shell am start -W -n " + app
    result = os.popen(cmd_line).readlines()
    for line in result:
        if "ThisTime:" in line:
            _time = re.search(r'\s\d+', line)
            print _time
            start_times["ThisTime"] = _time.group().strip()
        if "TotalTime:" in line:
            _time = re.search(r'\s\d+', line)
            start_times["TotalTime"] = _time.group().strip()
        if "WaitTime:" in line:
            _time = re.search(r'\s\d+', line)
            start_times["WaitTime"] = _time.group().strip()
    return start_times


# def list_times():
#     app_dic = get_apps()
#     for app in app_dic.keys():
#         start_time = get_times(app)
#         app_dic[app] = start_time
#         print app + ": " + str(app_dic[app])
#         time.sleep(0.5)
#         clear_recent()
#         #time.sleep(1)
#     return app_dic

def writeReportToHtml_name(htmlfile, appname, test_type):
    if "first" in test_type:
        htmlfile.write("<td> %s [First start]</td>\n"%appname)
    else:
        htmlfile.write("<td> %s [None First]</td>\n"%appname)

def writeReportToHtml_Begain(htmlfile):
    htmlfile.write("<tr>")

def writeReportToHtml_End(htmlfile):
    htmlfile.write("</tr>")
    
def writeReportToHtml_data(htmlfile, appname, app_dic, i, test_type):
    writeReportToHtml_Begain(htmlfile)
    writeReportToHtml_name(htmlfile, appname, test_type)
    htmlfile.write("<td> ThisTime </td>\n")
    
    aveValue = 0
    nonecount = 0
    for j in range(1, i+1, 1):
        if 1==j:
            if None==app_dic[appname]["ThisTime"]:
                aveValue += 0
                nonecount += 1
            else:
                aveValue += int(app_dic[appname]["ThisTime"])
            htmlfile.write("<td> %s </td>\n"%(app_dic[appname]["ThisTime"]))
        else:
            if None==app_dic[appname+"."+str(j)+".copytest"]["ThisTime"]:
                aveValue += 0
                nonecount += 1
            else:
                aveValue += int(app_dic[appname+"."+str(j)+".copytest"]["ThisTime"])
            htmlfile.write("<td> %s </td>\n"%(app_dic[appname+"."+str(j)+".copytest"]["ThisTime"]))
    if nonecount==i:
        aveValue = 0
    else:
        aveValue = aveValue/(i-nonecount)
    if "first" in test_type:
        htmlfile.write("<td class='tdimpotant'> %d </td>\n"%(aveValue))
    else:
        htmlfile.write("<td> %d </td>\n"%(aveValue))
    
    writeReportToHtml_End(htmlfile)
    writeReportToHtml_Begain(htmlfile)
    
    aveValue = 0
    nonecount = 0
    writeReportToHtml_name(htmlfile, "...", test_type)
    htmlfile.write("<td> TotalTime </td>\n")
    for j in range(1, i+1, 1):
        if 1==j:
            if None==app_dic[appname]["TotalTime"]:
                aveValue += 0
                nonecount += 1
            else:
                aveValue += int(app_dic[appname]["TotalTime"])
            htmlfile.write("<td> %s </td>\n"%(app_dic[appname]["TotalTime"]))
        else:
            if None==app_dic[appname+"."+str(j)+".copytest"]["TotalTime"]:
                aveValue += 0
                nonecount += 1
            else:
                aveValue += int(app_dic[appname+"."+str(j)+".copytest"]["TotalTime"])
            htmlfile.write("<td> %s </td>\n"%(app_dic[appname+"."+str(j)+".copytest"]["TotalTime"]))
    if nonecount==i:
        aveValue = 0
    else:
        aveValue = aveValue/(i-nonecount)
    if "first" in test_type:
        htmlfile.write("<td class='tdimpotant'> %d </td>\n"%(aveValue))
    else:
        htmlfile.write("<td> %d </td>\n"%(aveValue))
    
    writeReportToHtml_End(htmlfile)
    writeReportToHtml_Begain(htmlfile)
    
    aveValue = 0
    nonecount = 0
    writeReportToHtml_name(htmlfile, "...", test_type)
    htmlfile.write("<td> WaitTime </td>\n")
    for j in range(1, i+1, 1):
        if 1==j:
            if None==app_dic[appname]["WaitTime"]:
                aveValue += 0
                nonecount += 1
            else:
                aveValue += int(app_dic[appname]["WaitTime"])
            htmlfile.write("<td> %s </td>\n"%(app_dic[appname]["WaitTime"]))
        else:
            if None==app_dic[appname+"."+str(j)+".copytest"]["WaitTime"]:
                aveValue += 0
                nonecount += 1
            else:
                aveValue += int(app_dic[appname+"."+str(j)+".copytest"]["WaitTime"])
            htmlfile.write("<td> %s </td>\n"%(app_dic[appname+"."+str(j)+".copytest"]["WaitTime"]))
    if nonecount==i:
        aveValue = 0
    else:
        aveValue = aveValue/(i-nonecount)
    if "first" in test_type:
        htmlfile.write("<td class='tdimpotant'> %d </td>\n"%(aveValue))
    else:
        htmlfile.write("<td> %d </td>\n"%(aveValue))
    
    writeReportToHtml_End(htmlfile)

def filishHtmlFile(htmlfile):
    htmlfile.write("</table>\n</br></br></br></br>\n</center>\n</body>\n</html>")
    htmlfile.close()
    
def launch_app(app):
    thread_start = ThreadStartApp(app, static_usage.device_id)
    start_time = time.time()
    thread_start.start()
    thread_start.join(12)#waiting time out here
    now_time = time.time()
    time.sleep(1)
    get_start_times = thread_start.get_start_times()
    
    now_time = now_time - start_time
    if now_time >= 10:
        if thread_start.is_alive():
            kill_this_app(app)
        print "ERROR: this app cannot launch success : "+ app
        print "launch again"
        time.sleep(2)
        launch_app(app)
    else:
        return get_start_times
    
        
    
def write_html(app_choice_file, reportfilename):
    htmlfile = openHtmlFile(reportfilename)
    initHtml(htmlfile)
    print static_usage().report_file_p
    os.popen("echo begain: > "+static_usage().report_file_p).readlines()
    
    app_dic = get_apps(app_choice_file)
    need_run_count = len(app_dic)
    running_count = 0
    for app in app_dic.keys():
        running_count += 1
        print str(running_count)+"/"+str(need_run_count) +"-"+ app + ":"
         
        test_type = "first start"
        start_time = launch_app(app)
        app_dic[app] = start_time
        print app_dic[app]
        cmd_line = "echo " + app + " >> "+static_usage().report_file_p
        os.popen(cmd_line).readlines()
         
        cmd_line = "echo " + str(start_time) + " >> "+static_usage().report_file_p
        os.popen(cmd_line).readlines()
        home_exit_app()
        time.sleep(5)

    cmd_line = "echo -------------hot hit--------------- >> "+static_usage().report_file_p
    os.popen(cmd_line).readlines()
    app_names = list(app_dic.keys())
    for i in [13, 14, 5, 2, 14, 11, 8, 9, 1, 3, 0 , 12, 6, 5, 13, 7, 5, 6]:
        app = app_names[i]
        print app
        
        #judge is hot hit
        appinfo_temp = app.split("/")
        pakname = appinfo_temp[0].strip()
        #print("get package name:"+pakname)
        if isWindowsSystem():
            result = Popen("adb -s " + static_usage.device_id + " shell ps -A | findstr "+pakname, shell=True, stdout=PIPE).stdout.readlines()
        else:
            result = Popen("adb -s " + static_usage.device_id + " shell ps -A | grep "+pakname, shell=True, stdout=PIPE).stdout.readlines()
        
        hothit_type = "launching:cold+warm"
        if 0!=len(result):
            for r_line in result:
                if pakname+'\n' in r_line:
                    hothit_type = "launching:hot"
        print hothit_type
        start_time = launch_app(app)
        print start_time
        cmd_line = "echo " + app + " >> "+static_usage().report_file_p
        os.popen(cmd_line).readlines()
        
        cmd_line = "echo " + hothit_type + "  " + str(start_time) + " >> "+static_usage().report_file_p
        os.popen(cmd_line).readlines()
        home_exit_app()
        time.sleep(5)
    
    print "will look:" + static_usage().report_file_p
    
    filishHtmlFile(htmlfile)

def openHtmlFile(filename):
    htmlfile = open(filename,'w')
    return htmlfile

class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance  

class static_usage(Singleton):
    debug = False
    version_checking_server = "wukong.tclcom.com"
    version_checking_server_url = "http://wukong.tclcom.com/ftp/pub/performance/version_checking_server/"
    app_choice_file = "Apps_choice.txt"
    report_file = "appStartTimeTestReport.html"
    report_file_p = "appStartTime_hothit_test_report.html"
    device_id = ""
        
    def __init__(self):
        self.version = 1.1
        
    def help_usage(self):
        print "usage:"
        print "-h, (--help) : "
        print "-i, (--input) : the apps info file, default : Apps_choice.txt"
        print "-o, (--output) : the test output file, default : appStartTimeTestReport.html"
        print "-o2, (--hothitoutput) : the test output file, default : appStartTime_hothit_Test_Report.html"
    
    def version_usage(self):
        print "Version : "+str(self.version)
        
    def check_new_version(self):
        print "check new version online!!!"
        import httplib 
        conn = httplib.HTTPConnection(self.version_checking_server)
        conn.request("GET", self.version_checking_server_url)
        resp = conn.getresponse()
        data_version = ""
        if resp.status == 200:
            data_version = resp.read()
            conn.close()
            
            #print data_version
            version_file_name = "version_check_list.txt"
            version_file = open(version_file_name, "w")
            version_file.writelines(data_version)
            version_file.close()
            time.sleep(1)
            
            import ConfigParser
            try:
                conf=ConfigParser.ConfigParser()
                conf.read(version_file_name) 
                for sn in conf.sections():
                    #print sn
                    if __file__ in sn:
                        for attr in conf.options(sn):
                            #print attr+'='+conf.get(sn,attr)
                            if attr in "newest_version":
                                newest_version = conf.get(sn,attr)
                            elif attr in "download_url":
                                download_url = conf.get(sn,attr)
                                
                        if newest_version == str(self.version):
                            print "already newest version"
                        else:
                            print "the script already upgrade, please download newest one and test."
                            print "download: "+download_url
                            print ""
                            print ""
                            print ""
                            time.sleep(2)
                            sys.exit(0)
            except Exception, e:
                print e
            os.remove(version_file_name)
            
        else:
            print "cannot get version : "+self.version_checking_server_url + "  reason : "+resp.reason
            conn.close()
        


def check_inpute_parameter(argv):
    try:
        if len(argv) == 1:
            argv.append('-h')
        opts, args = getopt.getopt(argv[1:], 'hvdi:o:p:', ['input=','output=','puthothit='])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            static_usage().help_usage()
            sys.exit(1)
        elif opt in ('-v', '--version'):
            static_usage().version_usage()
            sys.exit(0)
        elif opt in ('-d', '--debug'):
            static_usage.debug = True
        elif opt in ('-o', '--output'):
            if arg != "" and len(arg) >= 1:
                static_usage.report_file = arg
        elif opt in ('-p', '--puthothit'):
            if arg != "" and len(arg) >= 1:
                static_usage.report_file_p = arg
        elif opt in ('-i', '--input'):
            if arg != "" and len(arg) >= 1:
                static_usage.app_choice_file = arg
        else:
            print 'unhandled option'
            sys.exit(3)

if __name__ == "__main__":
    
    check_inpute_parameter(sys.argv)
    #static_usage().check_new_version()
    if static_usage.device_id == "":
        device_id = SelectDevice().select_device()
        static_usage.device_id = device_id
         
    clear_recent()
     
    write_html(static_usage().app_choice_file, static_usage().report_file)
    print "the report file created: " + static_usage().report_file_p
    print "END!!!"

