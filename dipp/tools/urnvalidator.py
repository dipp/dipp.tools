#!/usr/bin/env python
#
# Checks if a URN of a given URN is registered at the DNB and if it is valid
#

__version__ = "$Id: urnvalidator 3066 2011-04-15 12:56:20Z reimer $"
__author__ = "Peter Reimer <reimer@hbz-nrw.de>" 

import httplib


RESOLVER = "nbn-resolving.de"

class URN:
    
    def __init__(self, urn, url):
        
        self.url = url
        self.urn = urn
        self.status, self.headers = self.get_dnb_status()

    def get_dnb_status(self):
        """ connect to the resolver of the DNB an return the HTTP
            status code and headers for a given URN
        """
        
        dnb = httplib.HTTPConnection(RESOLVER, 80)
        dnb.connect()
        dnb.request("HEAD", "/" + self.urn)
        res = dnb.getresponse()
        status = res.status
        headers = res.getheaders()
        dnb.close()
        return status, headers

    def is_registered(self):
        """a request for a registered URN is redirected to the registered
           URL with HTTP code 302. A not registered URN results in an error
           page with HTTP code 200.
        """
        
        if self.status == 302:
            return True
        else:
            return False

    def is_valid(self):
        """A URN is only valid, when the actual URL of the document and the
           registered URL are identical. http and https are considered to be
           the same url 
        """
        
        url = self.url.split('//')[-1] # chop of protocol
        if self.is_registered():
            reg_url = self.registered_url().split('//')[-1]
        else:
            reg_url = None
            
        if url == reg_url:
            return True
        else:
            return False
        
        
    def registered_url(self):
        """return the registered URL which is contained in the HTTP header
           of the redirected request
        """
        h = dict(self.headers)
        return h.get('location',None)
    
    
if __name__ == '__main__':
    
    URNs = (
        ("urn:nbn:de:0009-11-29231", "http://www.socwork.net/2011/1/salisbury"),
        ("urn:nbn:de:0009-11-29231", "http://www.socwork.net/2011/1/salisbury-wrong"),
        ("urn:nbn:de:0009-11-fake",  "http://www.socwork.net/2011/1/salisbury"),
        ("urn:nbn:de:0009-11-20391", "https://www.socwork.net/2009/1/special_issue/bailey")
    )
    
    for urn, url in URNs:
        x = URN(urn, url)
        print x.urn, x.is_registered(), x.is_valid(), x.registered_url(), x.url
    
        
