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
        top_headings = 0
        # the actual article text is wrapped in a <div class="section">We only need the first one
        main_section = soup.find("div", {"class":"section"})
        for h in main_section.findAll(self.headings):
            level = int(h.name[1:])
            anchor = h.find("a")
            if anchor:
                id = anchor.get('id',None)
            else:
                id = None
            toc.append((level, id, h.text))

        return toc
    
    
    def get_toc_html(self):
        
        toc = self.get_toc()
        root = etree.Element("ol")
        parent_level = 1
        
        for level, id, text in toc:
            delta = level - parent_level
            #print level, delta, text
            item = etree.SubElement(root, "li" )
            if id:
                link = etree.SubElement(item, "a", href=id )
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

