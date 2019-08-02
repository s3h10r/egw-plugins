#!/usr/bin/env python3
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
    "name" : "mosaic",
    "version" : "0.1.9",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class Mosaic(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'block_size' : 32 }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def run(self):
        return _mosaic(**self._kwargs)


filter = Mosaic()
assert isinstance(filter,EGWPluginFilter)


def _mosaic(image, block_size = 32):
    '''
    @param img: instance of Image
    @param block_size: [1, N]
    @return: instance of Image
    '''

    if image.mode != "RGBA":
        img = image.convert("RGBA")
    width, height = image.size
    pix = image.load()
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    for w in range(0, width, block_size):
        for h in range(0, height, block_size):
            r_sum, g_sum, b_sum = 0, 0, 0
            size = block_size ** 2
            for i in range(w, min(w+block_size, width)):
                for j in range(h, min(h+block_size, height)):
                    r_sum += pix[i, j][0]
                    g_sum += pix[i, j][1]
                    b_sum += pix[i, j][2]
            r_ave = int(r_sum / size)
            g_ave = int(g_sum / size)
            b_ave = int(b_sum / size)
            for i in range(w, min(w+block_size, width)):
                for j in range(h, min(h+block_size, height)):
                    dst_pix[i, j] = r_ave, g_ave, b_ave, pix[w, h][3]
    return dst_img
