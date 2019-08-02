#!/usr/bin/env python3
#coding=utf-8
import logging
import math
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
    "name" : "glowing_edge",
    "version" : "0.1.9",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class GlowingEdge(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def run(self):
        return _glowing_edge(**self._kwargs)


filter = GlowingEdge()
assert isinstance(filter,EGWPluginFilter)


def _glowing_edge(image):
    '''
    @效果：照亮边缘
    @param image: instance of Image
    @return: instance of Image
    '''
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    width, height = image.size
    pix = image.load()
    for w in range(width-1):
        for h in range(height-1):
            bottom = pix[w, h+1] # 下方像素点
            right = pix[w+1, h] # 右方像素点
            current = pix[w, h] # 当前像素点
            # 对r, g, b三个分量进行如下计算
            # 以r分量为例：int(2 * math.sqrt((r[current]-r[bottom])^2 + r[current]-r[right])^2))
            pixel = [int(math.sqrt((item[0] - item[1]) ** 2 + (item[0] - item[2]) ** 2) * 2)
                     for item in list(zip(current, bottom, right))[:3]]
            pixel.append(current[3])
            pix[w, h] = tuple([min(max(0, i), 255) for i in pixel]) # 限制各分量值介于[0, 255]
    return image
