# -*- coding: utf-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://dynamic2.scrape.center/'
browser.get(url)
logo = browser.find_element_by_class_name('logo-image')
print(logo)
print(logo.get_attribute('src'))
browser.close()
