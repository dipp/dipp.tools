#!/usr/bin/env python
#
# Checks if a URN of a given URN is registered at the DNB and if it is valid
#

__version__ = "$Id: urnvalidator 3066 2011-04-15 12:56:20Z reimer $"
__author__ = "Peter Reimer <reimer@hbz-nrw.de>" 

import httplib
import urllib
import urlparse
import xml.dom.minidom

RESOLVER = "nbn-resolving.org"

class URN:
    
    def __init__(self, urn, url):
        
        self.url = url
        self.urn = urn
        self.status = False
        self.headers = False


    def make_query_url(self):
        path = 'resolver'
        params = {"identifier":self.urn,"verb":"full","xml":"on"} 
        query = urllib.urlencode(params)
        query_url = urlparse.urlunparse(('http',RESOLVER,path,'',query,''))
        return query_url

    def get_dnb_response(self):
        """ connect to the resolver of the DNB an return the HTTP
            status code and headers for a given URN
        """
        
        conn = httplib.HTTPConnection(RESOLVER, 80)
        conn.request("GET", self.make_query_url())
        response = conn.getresponse()
        xml = response.read()
        return xml

    def is_registered(self):
        xmldoc = xml.dom.minidom.parseString(self.get_dnb_response())
        header = xmldoc.getElementsByTagName("pidef:header")[0]
        status_code = header.getElementsByTagName("pidef:status_code")[0]
        print status_code.firstChild.nodeValue
        data = xmldoc.getElementsByTagName("pidef:data")[0]
        url_infos = data.getElementsByTagName("pidef:url_info")
        for url_info in url_infos:
            url = url_info.getElementsByTagName("pidef:url")[0]
            print url.firstChild.nodeValue

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
        ("urn:nbn:de:0009-6-fake", "https://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-2480", "https://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-5890", "https://www.jvrb.org/past-issues/3.2006/589")
    )
   
    for urn, url in URNs:
        x = URN(urn, url)
        x.is_registered()
    
        
