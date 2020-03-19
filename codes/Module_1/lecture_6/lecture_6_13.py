# -*- coding: utf-8 -*-

from multiprocessing import Pool
import urllib.request
import urllib.error


def scrape(url):
    try:
        urllib.request.urlopen(url)
        print("URL {0} Scraped".format(url))
    except (urllib.error.HTTPError, urllib.error.URLError):
        print("URL {0} not Scraped".format(url))


if __name__ == "__main__":
    pool = Pool(processes=3)
    urls = [
        'https://www.dogedoge.com/',
        'https://www.csdn.net/',
        'https://bj.meituan.com/',
        'http://xxxyxxx.net'
    ]
    pool.map(scrape, urls)
    pool.close()
