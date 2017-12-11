#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of web-eremote-mini.
# https://github.com/garaemon/web-eremote-mini

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Ryohei Ueda <garaemon@gmail.com>

from preggy import expect

from web_eremote_mini import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
