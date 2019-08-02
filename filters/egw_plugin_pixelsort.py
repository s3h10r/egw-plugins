#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
egw-filter Pixelsort
"""
import logging
import math
import string
import sys
import colorsys
from PIL import Image

from einguteswerkzeug.plugins import EGWPluginFilter
from .pixelsort import do_pixelsort

fmeta = {
    "name" : "pixelsort",
    "version" : "0.1.9",
    "description" : "a filter which rearranges the pixels of an input image via sorting them by color",
    "author" : "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
}

class Pixelsort(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = {'algo' : 10}
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs

    def run(self):
        return do_pixelsort(**self._kwargs)


filter = Pixelsort(algo=1)

#print(filter.help)
#print(isinstance(filter_pixelsort, EGWPluginBase))
#print(isinstance(filter_pixelsort, EGWPluginFilter))
#print(isinstance(filter_pixelsort, EGWPluginGenerator))

assert isinstance(filter,Pixelsort)
assert issubclass(Pixelsort,EGWPluginFilter)
assert isinstance(filter,EGWPluginFilter)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage selftest: <me> image_in image_out")
    else:
        filter = Pixelsort(image = sys.argv[1], algo = 1)
        img = filter.run()
        img.save(sys.argv[2])
