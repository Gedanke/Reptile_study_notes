# -*- coding: utf-8 -*-


from newspaper import Article

url = 'https://tech.163.com/19/0909/08/EOKA3CFB00097U7S.html'
article = Article(url, language='zh')
article.download()
# print('html:', article.html)
article.parse()
print('authors:', article.authors)
print('title:', article.title)
print('date:', article.publish_date)
print('text:', article.text)
print('top image:', article.top_image)
print('movies:', article.movies)
article.nlp()
print('keywords:', article.keywords)
print('summary:', article.summary)
