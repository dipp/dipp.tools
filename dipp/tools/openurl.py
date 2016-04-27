# -*- coding: utf-8 -*-
from urllib import urlencode

class OpenURL:

    def __init__(self):
        self.ver = "Z39.88-2004"
        self.format = "info:ofi/fmt:kev:mtx:journal"
        
    def __make_author_parts__(self):
        
        parts = []
        authors = getattr(self, 'authors', ())
        if len(authors) > 0:
            parts.append(('rft.aulast', authors[0][0]))
            parts.append(('rft.aufirst', authors[0][1]))
        for lastname, firstname in authors:
            parts.append(('rft.au', lastname + ", " + firstname))
        
        return parts
    
    def __make_object_parts__(self):
        
        metadata = (
            ('ctx_ver', '', self.ver),
            ('rft_val_fmt', '', self.format),
            ('rft_id', 'info:doi/', getattr(self, 'doi', '')),
            ('rft_id', 'info:urn/', getattr(self, 'urn', '')),
            ('rft_id', '', getattr(self, 'url', '')),
            ('rft.atitle', '', getattr(self, 'atitle', '')),
            ('rft.jtitle', '', getattr(self, 'jtitle', '')),    
            ('rft.stitle', '', getattr(self, 'stitle', '')),    
            ('rft.volume', '', getattr(self, 'volume', '')),    
            ('rft.issn', '', getattr(self, 'issn', '')),    
            ('rft.issue', '', getattr(self, 'issue', '')),    
            ('rft.date', '', getattr(self, 'date', '')),    
        )
        
        parts = []
        for key, prefix, value in metadata:
            if value:
                parts.append((key, prefix + value))
        return parts
        
    def geturl(self):
        
        kv = []
        for k, v in self.__make_object_parts__() + self.__make_author_parts__():
            if v:
                kv.append(urlencode({k:v}))
        url = '&'.join(kv)
        return url
        
    def getcoins(self):
        coins = '<span class="Z3988" title="%s">COinS</span>' % self.geturl()
        return coins
    
if __name__ == '__main__':
    
    ou = OpenURL()
    # ou.atitle = "ohne umlaute"
    ou.atitle = "mit Ümläüte"
    ou.stitle = "joe"
    print ou.getcoins()
    
