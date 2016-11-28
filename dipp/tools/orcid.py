#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
try:
    import json
except ImportError:
    import simplejson as json

class Orcid:

    def __init__(self, cmd):
        
        self.cmd = cmd

    def read(self, orcidid):
        process = Popen([self.cmd, '-o', orcidid, 'bio'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        
        return json.loads(stdout)

if __name__ == '__main__':

    ORCID = "/files/lib/python-2.7-dev/bin/orcid"

    o = Orcid(ORCID)
    print o.read("0000-0002-3187-2536")
