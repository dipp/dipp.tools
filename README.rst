dipp.tools
##########

Various python tools for use with the DiPP Publishing Platform

- Creation of OpenURLs
- Validation of URNs
- Indentation and prettyprinting of XML strings

Installation
************

The module is installed by running::

    $ easy_install -f http://alkyoneus.hbz-nrw.de/dist -U dipp.tools
    
The command adds the module to your site-package directory and installs a
commandline program.

Usage
*****

Commandline
===========

The command ``urnvalidator`` can be used to check the validity of an URN::

   $ urnvalidator -h
   usage: urnvalidator [-h] [-l] [-n]
   
   check if the URN is registered with the DNB
   
   optional arguments:
     -h, --help  show this help message and exit
     -l, --url   the objects actual URL
     -n, --urn   the objects URN
      
Example::

   $ urnvalidator -u http://www.dipp.nrw.de/lizenzen/dppl/fdppl/f-DPPL_v3_en_11-2008.html urn:nbn:de:0009-fdppl-v3-en3
   urn:nbn:de:0009-fdppl-v3-en3 registered and valid url
   
   