#!/usr/bin/env python
#
# Checks if a URN of a given URN is registered at the DNB and if it is valid
#

__version__ = "$Id: urnvalidator 3066 2011-04-15 12:56:20Z reimer $"
__author__ = "Peter Reimer <reimer@hbz-nrw.de>" 

import argparse
import httplib
import urllib
import urlparse
import xml.dom.minidom

RESOLVER = "nbn-resolving.org"

class URN:
    
    def __init__(self, urn, url):
        
        self.url = url
        self.urn = urn
        self.query_url = self.make_query_url()


    def make_query_url(self):
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
        
        pidef = {"header":None, "data":None, "valid": False}
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
        urls = []
        if len(url_infos_elems) > 0:
            for url_infos_elem in url_infos_elems:
                url_info = {}
                for x in ('url','created','last_modified'):
                    url_info[x] = getChildrenByName(url_infos_elem, ":".join(("pidef",x)))[0].firstChild.nodeValue
                data.append(url_info)
                urls.append(url_info["url"].split('//')[-1])
            # check validity
            if urls[0] == self.url.split('//')[-1]: 
                pidef["valid"] = True
        
        pidef["data"] = data
        return pidef

def getChildrenByName(element, name):
    children = []
    for child in element.childNodes:
        if child.nodeName == name:
            children.append(child)
    return children

def main():

    parser = argparse.ArgumentParser(description='check if the URN is registered with the DNB')
    parser.add_argument("-l", "--url", action='store_true', help='the objects actual URL')
    parser.add_argument("-n", "--urn", action='store_true', help='the objects URN')
    args = parser.parse_args()

    URNs = (
        ("urn:nbn:de:0009-6-fake", "https://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-2480", "https://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-5890", "https://www.jvrb.org/past-issues/3.2006/589")
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
                print count, url_info['url']
if __name__ == '__main__':
    main()
    
    
        
