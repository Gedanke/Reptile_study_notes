# -*- coding: utf-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://dynamic2.scrape.center/'
browser.get(url)
input = browser.find_element_by_class_name('logo-title')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)
browser.close()
