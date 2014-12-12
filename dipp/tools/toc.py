#!/usr/bin/env python
from lxml.html import fromstring

f = open('article.html','r')
html = f.read()
f.close()

tree = fromstring(html)

for a in tree.cssselect('h3 a'):
    print 'found "%s" link to href "%s"' % (a.text, a.get('id'))
