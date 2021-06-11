# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

ip = '127.0.0.1'
port = 8889
username = 'foo'
password = 'bar'

manifest_json = """{"version":"1.0.0","manifest_version": 2,"name":"Chrome Proxy","
permissions": ["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],"background":
{"scripts": ["background.js"]
} }
"""
background_js = """
var config = { mode: "fixed_servers", rules: { singleProxy: { scheme: "http", host: "%(ip) s", port: %(port) s } } }

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) { return { authCredentials: {username: "%(username) s", password: "%(password) s"
} } }

chrome.webRequest.onAuthRequired.addListener(
callbackFn, {urls: ["<all_urls>"]},
['blocking']
)
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}

plugin_file = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
zp.writestr("background.js", background_js)
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_extension(plugin_file)
browser = webdriver.Chrome(options=options)
browser.get('https://httpbin.org/get')
print(browser.page_source)
browser.close()
