# -*- coding: utf-8 -*-

import newspaper

source = newspaper.build('http://www.sina.com.cn/', language='zh')
for category in source.category_urls():
    print(category)
for article in source.articles:
    print(article.url)
    print(article.title)

for feed_url in source.feed_urls():
    print(feed_url)
