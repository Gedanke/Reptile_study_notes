# -*- coding: utf-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://dynamic2.scrape.center/')
output = browser.find_element_by_class_name('logo-image')
print(output)
browser.close()
