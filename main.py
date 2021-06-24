import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
import time
import lxml
import json
from bs4 import BeautifulSoup as bs
from requests_html  import HTMLSession
import re
import os
import datetime
from selenium import webdriver

def submit(): #提交订单函数
    is_done = 0
    session  = HTMLSession()
    try:
        
        browser = webdriver.Chrome(executable_path="chromedriver.exe")

        baseURL='https://tk.lenovo.com.cn/product/1014423.html'
        
        browser.get(baseURL)
        #time.sleep(1)
        time.sleep(10)
        html = browser.page_source
        s = bs(html, 'html.parser')
        tar = s.find(id="ljgm")
        result = tar['title']
        
        
        print(datetime.datetime.now()," : ",result)
        
        login = browser.find_element_by_xpath("//a[@class='login']")
        login.click()
        
        time.sleep(1)
        
        mode = browser.find_element_by_xpath("//a[@class='login_type login_account']")
        mode.click()
        
        time.sleep(1)
        
        us = browser.find_element_by_xpath("//input[@class='input account']")
        us.send_keys("你的联想账号")
        pw = browser.find_element_by_xpath("//input[@class='input pwd']")
        pw.send_keys("你的联想密码") 
        
        time.sleep(1)
        
        bt = browser.find_element_by_xpath("//a[@class='submit']")
        bt.click()
        
        time.sleep(3)
        
        ele = browser.find_element_by_id("ljgm")
        ele.click()
        
        time.sleep(5)
        
        #ele.click()
        #ele=browser.find_element_by_class_name("fr submitBtn")
        
        ele=browser.find_element_by_xpath("//span[@class='fr submitBtn']")
        ele.click()
        time.sleep(2)
        print("成功提交订单")
        time.sleep(10)
        
        
        return True,ele

    except Exception as e:
        print(e)
        return False,e
    
def alertMail(info=""): #发送email通知函数

     
    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="xxxxxxxxxx"    #用户名
    mail_pass="xxxxxxxx"   #SMTP口令 
     
     
    sender = 'xxxxxxxx' #和user一样
    receivers = ['xxxxxx']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
     
    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("SMTP", 'utf-8')
    message['To'] =  Header("测试", 'utf-8')
     
    subject = 'STMP提醒:'+info
    message['Subject'] = Header(subject, 'utf-8')
     
     
    try:
        smtpObj = smtplib.SMTP() 
        print(1)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        print(2)
        smtpObj.login(mail_user,mail_pass)  
        print(3)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print(4)
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
        
def watch(browser): #监控函数
   
    baseURL='https://tk.lenovo.com.cn/product/1014423.html'
    #baseURL='https://tk.lenovo.com.cn/product/1014422.html'
    
    #response = session.get(baseURL)
    #print(response.html.render())
    #headers={'Cookie':cookie}
    #req = requests.get(url=baseURL,headers=headers)
    browser.get(baseURL)
    #time.sleep(1)
    
    i=0
    while(True):
        time.sleep(1)
        i=i+1
        if(i>20):
            return False,"???"
        html = browser.page_source
        s = bs(html, 'html.parser')
        #arrivalTime_cities ljgm
        #s.find(id="arrivalTime_cities")
        tar = s.find(id="ljgm")
        try:
            result = tar['title']
            break
        except KeyError:
            continue
    
    print(datetime.datetime.now()," : ",result)
    if (result == "已抢光" or "已售罄"):
        return False,result
    else:
        
        return True,result
    
    
#主逻辑
is_done = 0
session  = HTMLSession()
browser = webdriver.PhantomJS()
print("start!")
while(True):
    state,result = watch(browser)
    if(state):
        #alertMail(result)
        if(is_done == 0):
            alertMail(result)
            s,i = submit()
            if(s==False):
                s,i=submit()
                if(s==False):
                    print("提交2次订单失败",i)
        is_done+=1
        if(is_done>80):
            is_done = 0
            
        #break
    else:
        is_done = 0
        time.sleep(10)
