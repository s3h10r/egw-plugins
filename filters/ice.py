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
    "name" : "ice",
    "version" : "0.1.9",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class Ice(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def _generate_image(self):
        return self._ice(**self._kwargs)


    def _ice(self,image):
        '''
        @效果：冰冻
        @param image: instance of Image
        @return: instance of Image
        '''
        if image.mode != "RGB":
            image.convert("RGB")
        width, height = image.size
        pix = image.load()
        for w in range(width):
            for h in range(height):
                r, g, b = pix[w, h]
                pix[w, h] = min(255, int(abs(r - g - b) * 3 / 2)), \
                            min(255, int(abs(g - b - r) * 3 / 2)), \
                            min(255, int(abs(b - r - g) * 3 / 2))
        return image


filter = Ice()
assert isinstance(filter,EGWPluginFilter)
