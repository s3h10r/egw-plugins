#!/usr/bin/env python3
#coding=utf-8
import logging
import random
import string
from PIL import Image
from einguteswerkzeug.helpers.gfx import get_exif, scale_image_to_square, scale_image, scale_square_image, trim
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
    "name" : "diffuse",
    "version" : "0.1.9",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class Diffuse(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'degree' : random.randint(1,32), }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _diffuse(**self.kwargs)


filter = Diffuse()
assert isinstance(filter,EGWPluginFilter)

def _diffuse(image, degree = 32):
    '''
    @效果：扩散
    @param image: instance of Image
    @param degree: 扩散范围，大小[1, 32]
    @return: instance of Image
    '''
    degree = min(max(1, degree), 32)
    width, height = image.size
    dst_image = Image.new(image.mode, (width, height))
    pix = image.load()
    dst_pix = dst_image.load()
    for w in range(width):
        for h in range(height):
            # 随机获取当前像素周围一随机点
            x = w + random.randint(-degree, degree)
            y = h + random.randint(-degree, degree)
            # 限制范围
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            dst_pix[w, h] = pix[x, y]
    return dst_image

filter = Diffuse()
assert isinstance(filter,EGWPluginFilter)
