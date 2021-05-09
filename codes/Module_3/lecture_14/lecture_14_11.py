# -*- coding: utf-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://dynamic2.scrape.center/'
browser.get(url)
input = browser.find_element_by_class_name('logo-title')
print(input.text)
browser.close()
