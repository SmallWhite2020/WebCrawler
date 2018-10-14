#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
import pdfkit
import random
import os
import time
import logging
import logging.config
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lxml import etree

def csdn(url):
    print('CSDN')
    option = webdriver.FirefoxOptions()


    time.sleep(3)
    driver = webdriver.Firefox(firefox_options=option)
    driver.implicitly_wait(15)
    driver.header_overrides = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Connection': 'keep-alive',
        'Referer': 'https://blog.csdn.net/haibo0668/article/details/80025077'}
    driver.get(url)
    print("a1")
    cookie_ori = driver.get_cookies()
    print(cookie_ori)
    print(type(cookie_ori))
    print(len(cookie_ori))
    cookie_ori_len = len(cookie_ori)
    l=[]
    for i in range(cookie_ori_len):
        # print(cookie_ori[i]['name'])
        name = cookie_ori[i]['name']
        # print(cookie_ori[i]['value'])
        value = cookie_ori[i]['value']
        t = (name,value)
        print(t)
        l.append(t)
    print(l)
    options = {
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept', '*/*'),
            ('Accept-Language', 'zh-CN,zh;q=0.9'),
            ('Cache-Control', 'max-age=0'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'),
            ('Connection', 'keep-alive'),
            ('Referer', 'https://blog.csdn.net/haibo0668/article/details/80025077'),
            ('Accept-Encoding','gzip, deflate, br'),
            ('Host','img-blog.csdn.net')
        ],
        'cookie':l
    }
    locator = (By.ID, "btn-readmore")
    randomInt = random.randint(0, 10)
    fileName = 'pdffile' + str(randomInt) + '.pdf'
    print('filename + ' + str(fileName))
    try:
        WebDriverWait(driver, 15, 0.5).until(EC.presence_of_element_located(locator))
        print('阅读更多按钮找到')
    except Exception as e:
        print(e)
        print("等待错了")
        pass
    try:
        time.sleep(2)
        print("开始爬取网页")
        logging.warning("开始爬取网页")
        time.sleep(3)
        html = driver.page_source
        print(type(html))
        print(html)
        time.sleep(2)
        print("找阅读更多按钮")
        try:
            target = driver.find_element_by_id("btn-readmore")
            driver.execute_script("arguments[0].scrollIntoView();", target)
            target.click()
            print("找阅读更多按钮OK")
            html = driver.page_source
            print(type(html))
        except Exception as e:
            print(e)
        try:
            time.sleep(1)
            print("找main Body")
            content_div = etree.HTML(html).xpath('//div[@class="blog-content-box"]')[0]
            content_byte = etree.tostring(content_div)
            content_str = bytes.decode(content_byte)
            html = content_str
            print("找main Body OK")
            time.sleep(1)
        except Exception as e:
            print(e)
        print('test' + str(fileName))
        pdfkit.from_string(html, fileName, options=options)
        print(fileName)


    except Exception as e:
        print(e)
        print("大概率按钮没找到")
        try:
            print('test' + str(fileName))
            print("pdf2")
            pdfkit.from_string(html, fileName, options=options)
            print(fileName)
            print("pdf")
        except Exception as e:
            print(e)
    print("OK4")
    driver.quit()


def wechat(url):
    print('non-CSDN')
    logging.warning('non-CSDN')
    # 开始爬取第一个页面（改成调用爬取程序）
    options = {
        'encoding': "utf-8",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    answer = 0
    try:
        print("开始爬取网页")
        logging.warning("开始爬取网页：" + url)
        response = requests.get(url, headers=headers)
    except:
        print("url请求待爬取网页失败")
        logging.warning("url请求待爬取网页失败：" + url)
        answer = 0
        pass
    else:
        soup = BeautifulSoup(response.content, "lxml")
        body = soup.find("html")
        imgs = body.find_all("img")
        for img in imgs:
            data_src = img.get('data-src')
            if data_src != None:
                img['src'] = str(data_src)
        randomInt = random.randint(0, 10)
        fileName = 'pdffile' + str(randomInt) + '.pdf'
        print(fileName)
        try:
            print("开始转换htmlTo")
            logging.warning("开始转换htmlTo")
            pdfkit.from_string(str(body), fileName, options=options)
        except IOError:
            pass #出现IOError忽略
        except:#忽略一些异常
            pass
        #判断是否生成pdf文件
        filepath = './' + fileName
        print(filepath)
        answer = os.path.exists(filepath)
        print(answer)
        #正常的调用上传接口
    if answer == True:
        print("生成文件名称是： " + fileName)
        logging.warning("生成文件名称是： " + fileName)
        return fileName
    else:
        return 0

if __name__ == "__main__":


    print(csdn('https://img-blog.csdn.net/20161103142331865?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center'))

