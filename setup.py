from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

__version__ = read('version.txt').strip()
__author__ = "Peter Reimer"

setup(name='dipp.tools',
      version=__version__,
      description="dipp tools",
      long_description=read('README'),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author=__author__,
      author_email='reimer@hbz-nrw.de',
      url='http://www.dipp.nrw.de',
      license='DFSL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['dipp', 'dipp.tools'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
