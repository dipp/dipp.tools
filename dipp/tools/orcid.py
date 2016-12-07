#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import PIPE, Popen
from distutils.spawn import find_executable
import logging

logger = logging.getLogger('orcid')

try:
    import json
except ImportError:
    import simplejson as json

class Orcid:

    def __init__(self, path):
        
        self.executable = find_executable('orcid', path=path)
        if not self.executable:
            print "orcid not found"
        

    def read(self, resource, orcid_id):
    
        orcid_call = ' '.join([self.executable, '-o', orcid_id, resource])
        p = Popen(orcid_call, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                      close_fds=False)
        
        (fi, fo, fe) = (p.stdin, p.stdout, p.stderr)
        
        result = fo.read()
        fo.close()
        return json.loads(result)


if __name__ == '__main__':

    ORCID_PATH = "/files/lib/python-2.7-dev/bin"
    orcid_id = "0000-0002-3187-2536"
    
    o = Orcid(ORCID_PATH)
    print o.read("works", orcid_id)
    # orcid_call = ' '.join([ORCID, '-o', orcidid, 'works'])
    # print orcid_call
    
