#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install
from setuptools import setup, find_packages
import os

class inst(install):
    def run(self):
        install.run(self)

setup(
    name='scripts-teleservices',
    author='Nicolas Hislaire',
    author_email='nicolas.hislaire@imio.be',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/IMIO/scripts-teleservices',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    cmdclass={
        'inst': inst,
    }
)
