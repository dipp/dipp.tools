#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
from lxml import etree


class Toc:

    def __init__(self, html, levels=2):
        
        self.html = html
        self.levels = levels
        self.headings = [ "h%s" % i for i in range(1, self.levels + 1) ]

    def get_toc(self):
        soup = BeautifulSoup(self.html)
        toc = []
        for h in soup.findAll(self.headings):
            level = int(h.name[1:])
            anchor = h.find("a")
            if anchor:
                id = anchor.get('id',None)
            else:
                id = None
            toc.append((level, id, h.text))

        return toc
    
    def get_toc_html(self):
        
        toc = x.get_toc()
        root = etree.Element("ol")
        for level, id, text in toc:
            item = etree.SubElement(root, "li" )
            if id:
                link = etree.SubElement(item, "a", href=id )
                link.text = text
            else:
                item.text = text
        return etree.tostring(root, pretty_print=True)


if __name__ == '__main__':
    f = open('article.html','r')
    html = f.read()
    f.close()
    
    x = Toc(html,levels = 4)
    print x.get_toc_html()
