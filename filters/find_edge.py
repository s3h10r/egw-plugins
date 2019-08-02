#!/usr/bin/env python3
#coding=utf-8
import logging
import math
import string
from PIL import Image
from einguteswerkzeug.plugins import EGWPluginFilter
from .adjustment import invert
from .utils import Matrix33

fmeta = {
    "name" : "find_edge",
    "version" : "0.1.9",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class FindEdge(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'angle' : 60 }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def run(self):
        return _find_edge(**self._kwargs)


filter = FindEdge()
assert isinstance(filter,EGWPluginFilter)


def _find_edge(image, angle = 60):
    '''
    @效果：查找边缘
    @param image: instance of Image
    @param angle: 角度，大小[0, 360]
    @return: instance of Image
    '''

    radian = angle * 2.0 * math.pi / 360.0
    pi4 = math.pi / 4.0
    matrix33 = [
        [int(math.cos(radian + pi4) * 256),
         int(math.cos(radian + 2.0 * pi4) * 256),
         int(math.cos(radian + 3.0 * pi4) * 256)],
        [int(math.cos(radian) * 256),
         0,
         int(math.cos(radian + 4.0 * pi4) * 256)],
        [int(math.cos(radian - pi4) * 256),
         int(math.cos(radian - 2.0 * pi4) * 256),
         int(math.cos(radian - 3.0 * pi4) * 256)]
        ]
    m = Matrix33(matrix33, scale=256)
    img = m.convolute(image) # 对图像进行3*3卷积转换
    return invert(image) # 对图像进行负像处理
