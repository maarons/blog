#!/usr/bin/env python

from __future__ import print_function
from pygments.formatters import HtmlFormatter
import sys
from os.path import join, abspath

with open(join(abspath(sys.path[0]), "_pygments.scss"), "w") as f:
    print(HtmlFormatter().get_style_defs(".codehilite"), file = f)
