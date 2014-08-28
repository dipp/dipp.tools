#!/usr/bin/env python
#
# Checks if a URN of a given URN is registered at the DNB and if it is valid
#

__version__ = "$Id$"
__author__ = "Peter Reimer <reimer@hbz-nrw.de>" 

import argparse
import httplib
import urllib
import urlparse
import xml.dom.minidom

RESOLVER = "nbn-resolving.org"

class URN:
    
    def __init__(self, urn, url):
        
        self.url = https_to_http(url)
        self.urn = urn
        self.query_url = self.make_query_url()


    def make_query_url(self):
        """Construct the query URL for full XML response."""
        path = 'resolver'
        params = {"identifier":self.urn,"verb":"full","xml":"on"} 
        query = urllib.urlencode(params)
        query_url = urlparse.urlunparse(('http',RESOLVER,path,'',query,''))
        return query_url

    def get_dnb_response(self):
        """ connect to the resolver of the DNB an return the xml representation
            of the resolved URN 
        """
        
        conn = httplib.HTTPConnection(RESOLVER, 80)
        conn.request("GET", self.query_url)
        response = conn.getresponse()
        xml = response.read()
        return xml
    
    def parse_dnb_response(self):
        """Parse the XML Response coming from the DNB resolver.
        
        validity
        0: not registered
        1: registered and valid url 
        2: registered but invalid url
        """
        
        pidef = {"header":None, "data":None, "valid": 0}
        header = {}
        data = []
        xmldoc = xml.dom.minidom.parseString(self.get_dnb_response())
        
        # get header element
        header_elem = xmldoc.getElementsByTagName("pidef:header")[0]
        status_code_elem = header_elem.getElementsByTagName("pidef:status_code")[0]
        header["status_code"] = status_code_elem.firstChild.nodeValue
        pidef["header"] = header

        # get data element
        data_elem = xmldoc.getElementsByTagName("pidef:data")[0]
        url_infos_elems = data_elem.getElementsByTagName("pidef:url_info")
        if len(url_infos_elems) > 0:
            for url_infos_elem in url_infos_elems:
                url_info = {}
                
                for x in ('url','created','last_modified'):
                    url_info[x] = getChildrenByName(url_infos_elem, ":".join(("pidef",x)))[0].firstChild.nodeValue
                
                # mark the currently activ URL                
                if https_to_http(url_info['url']) == self.url:
                    url_info['current'] = True
                else:
                    url_info['current'] = False
                data.append(url_info)
                
            # check validity
            if data[0]['current'] == True: 
                pidef["valid"] = 1
            else:
                pidef["valid"] = 2
        
        pidef["data"] = data
        return pidef

def getChildrenByName(element, name):
    children = []
    for child in element.childNodes:
        if child.nodeName == name:
            children.append(child)
    return children

def https_to_http(url):
    """Convert an SSL URL to non-SSL URL."""
    parts = url.split('://')
    if len(parts) == 2:
        if parts[0].lower() == 'https': parts[0] = 'http'
        url = ('://').join(parts) 
    else:
        url = url
    return url  

def validate():
    """"Commandline interface."""
    validity = {
        0 : "not registered",
        1 : "registered and valid url", 
        2 : "registered but invalid url"
    }

    parser = argparse.ArgumentParser(description='Check if the URN is registered with the DNB.')
    parser.add_argument("-u", "--url", default='', help='The objects actual URL.')
    parser.add_argument("urn", help="URN (Uniform Resource Name) you want to validate.")
    
    args = parser.parse_args()
    urn = args.urn
    url = args.url
    
    x = URN(urn, url)
    answer = x.parse_dnb_response()
    valid = answer['valid']
    print urn, validity[valid]
  

def main():

    URNs = (
        ("urn:nbn:de:0009-6-fake", "https:/www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-2480", "HTTPs://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-5890", "http://www.jvrb.org/past-issues/3.2006/589")
    )
   
    for urn, url in URNs:
        x = URN(urn, url)
        answer = x.parse_dnb_response()
        print "### %s ###" % urn
        print "url: %s" % x.url
        print "status_code: %s" % answer["header"]["status_code"] 
        print "valid: %s" % answer["valid"] 
        if len(answer["data"]) == 0:
            print "no data found"
        else:
            for count, url_info in enumerate(answer["data"]):
                print count, url_info['url'], url_info['current'] 
                
if __name__ == '__main__':
    main()
    
    
        
