#!/usr/bin/env python
#
# Setup script for the dipp tools
# $Id: setup.py 4903 2014-08-28 09:28:52Z reimer $
#
# Usage: python setup.py install
#

from setuptools import setup, find_packages
from dipp.tools import __version__

def _read(doc):
    return open(doc, 'rb').read()

setup(
    name='dipp.tools',
    version=__version__,
    author="Peter Reimer",
    author_email='reimer@hbz-nrw.de',
    description="dipp tools",
    long_description=_read('README.rst').decode('utf-8'),
    install_requires=[
        'setuptools',
        'argparse',
        # -*- Extra requirements: -*-
    ],
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 2.4",
    ],
    keywords='',
    url='http://www.dipp.nrw.de',
    license='DFSL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['dipp', 'dipp.tools'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':[
            'urnvalidator=dipp.tools.urnvalidator:validate'
        ]
    },
)
