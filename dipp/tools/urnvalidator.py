#!/usr/bin/env python
#
# Checks if a URN of a given URN is registered at the DNB and if it is valid
#

__version__ = "$Id$"
__author__ = "Peter Reimer <reimer@hbz-nrw.de>"

import argparse
import httplib
import urllib2
import urllib
import urlparse
import logging
from BeautifulSoup import BeautifulSoup

RESOLVER = "nbn-resolving.org"
logger = logging.getLogger(__name__)


class URN:

    def __init__(self, urn, url):

        self.url = url
        self.urn = urn
        self.xml = self._get_dnb_response()
        self.details = None
        self.validity = 0
        if self.xml:
            self.details, self.validity = self._parse_dnb_response()

    def _get_dnb_response(self):
        """Connect to the resolver of the DNB an return the xml representation
           of the resolved URN
        """
        query_url = urlparse.urlunparse(('https', RESOLVER, self.urn, '', '', ''))
        logger.info("Resolving %s " % query_url)
        req = urllib2.Request(query_url)
        req.add_header('Accept', 'text/xml')
        try:
            resp = urllib2.urlopen(req)
            content = resp.read()
            return content
        except urllib2.HTTPError, e:
            logger.info(e)
            return None

    def _parse_dnb_response(self):

        soup = BeautifulSoup(self.xml)
        url_infos = []
        validity = 2
        resolving_information = soup.find('pidef:resolving_information')

        for info in resolving_information.findAll('pidef:url_info'):
            x = {'current': False}
            for key in ['url', 'created', 'last_modified']:
                x[key] = info.find('pidef:%s' % key).text
            if x['url'] == self.url:
                x['current'] = True
                validity = 1

            url_infos.append(x)
        return url_infos, validity


def validate():
    """"Commandline interface."""
    validity = {
        0: "not registered",
        1: "registered and valid url",
        2: "registered but invalid url"
    }

    parser = argparse.ArgumentParser(description='Check if the URN is registered with the DNB.')
    parser.add_argument("-u", "--url", default='', help='The objects actual URL.')
    parser.add_argument("urn", help="URN (Uniform Resource Name) you want to validate.")

    args = parser.parse_args()
    urn = args.urn
    url = args.url

    status = URN(urn, url)
    valid = status.validity
    print urn, validity[valid]


def main():

    console = logging.StreamHandler()
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

    URNs = (
        ("urn:nbn:de:0009-6-fake", "https://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-2480", "HTTPs://www.jvrb.org/past-issues/2.2005/248"),
        ("urn:nbn:de:0009-6-5890", "http://www.jvrb.org/past-issues/3.2006/589"),
        ("urn:nbn:de:0009-12-7036", "http://www.elogistics-journal.de/archiv/2005/11/zeitverhalten"),
        ("urn:nbn:de:0009-12-7036", "http://www.logistics-journal.de/not-reviewed/2005/11/zeitverhalten"),
    )

    for urn, url in URNs:
        x = URN(urn, url)
        print urn, x.validity
        if x.details:
            for detail in x.details:
                print detail['url'], detail['current'], detail['created'], detail['last_modified']


if __name__ == '__main__':
    main()
