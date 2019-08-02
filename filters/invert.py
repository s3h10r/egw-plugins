#!/usr/bin/env python
#coding=utf-8
import logging
import string
from PIL import Image
from einguteswerkzeug.plugins import EGWPluginFilter

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

fmeta = {
    "name" : "invert",
    "version" : "0.1.1",
    "description" : "inverts each pixel of the image",
    "author" : "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
}

class Invert(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def run(self):
        return _ice(**self._kwargs)


filter = Invert()
assert isinstance(filter,EGWPluginFilter)

def _invert(image = None):
    return image.point(lambda x: 255 - x)
