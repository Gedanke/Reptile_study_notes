# -*- coding: utf-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
print(browser.page_source)
browser.close()
