#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
from lxml import etree


class TOC:

    def __init__(self, html, levels=2):
        
        self.html = html
        self.levels = levels
        self.headings = [ "h%s" % i for i in range(1, self.levels + 1) ]

    def get_toc(self):
        soup = BeautifulSoup(self.html)
        toc = []

        # rip out first titlepage, since it contains headings 
        # and article metadate not belonging to the toc
        titlepage = soup.find("div", {"class":"titlepage"})
        titlepage.extract()
        
        for heading in soup.findAll(self.headings):
            level = int(heading.name[1:])
            anchor = heading.find("a")
            if anchor:
                id = anchor.get('id',None)
            else:
                id = None
            toc.append((level, id, heading.text))
        
        return toc
    
    
    def get_toc_html(self):
        
        toc = self.get_toc()
        root = etree.Element("ol")
        parent_level = 1
        
        for level, id, text in toc:
            delta = level - parent_level
            attrib = {"class":"toclevel%s" % (level - 1) }
            item = etree.SubElement(root, "li", attrib=attrib )
            if id:
                anchor = "#" + id
                link = etree.SubElement(item, "a", href=anchor )
                link.text = text
            else:
                item.text = text
            parent_level = level
        return etree.tostring(root, pretty_print=True)


if __name__ == '__main__':
    f = open('article.html','r')
    html = f.read()
    f.close()
    
    toc = TOC(html,levels = 4)
    print toc.get_toc_html()

