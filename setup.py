#!/usr/bin/env python

import os
import sys

import TestRunner


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [ 'TestRunner' ]

with open('README.md') as f:
    readme = f.read()
    f.close()

with open('LICENSE.txt') as f:
    LICENSE = f.read()
    f.close()


setup(
    name = TestRunner.__name__,
    version = TestRunner.__version__, # get the version of module from __init__ file.
    
    description ='Test Result Generator',
    
    author = TestRunner.__author__, # get the author of module from __init__ file.
    long_description = readme , # put the description after reading from README.txt file.
    author_email = TestRunner.__email__,
    url = TestRunner.__url__ ,
    packages = packages, # packages names which is to be installed.
    
    license = LICENSE ,
    
    classifiers=(
                'Development Status :: 5.3 - Production/Stable',
                'Intended Audience :: Developers/Automation Engineers',
                'Natural Language :: English',
                'License :: Apache 2.0',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4.1',
                ),
    )
