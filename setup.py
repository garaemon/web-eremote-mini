#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of web-eremote-mini.
# https://github.com/garaemon/web-eremote-mini

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Ryohei Ueda <garaemon@gmail.com>

from setuptools import setup, find_packages
from web_eremote_mini import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='web-eremote-mini',
    version=__version__,
    description='Web UI for eremote mini',
    long_description='''
Web UI for eremote mini
''',
    keywords='IoT',
    author='Ryohei Ueda',
    author_email='garaemon@gmail.com',
    url='https://github.com/garaemon/web-eremote-mini',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'broadlink',
        'flask',
        'plyvel',
        'pylint',
        'fire',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'web-eremote-mini=web_eremote_mini.cli:main',
        ],
    },
)
