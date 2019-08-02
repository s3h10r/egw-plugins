#!/usr/bin/env python3
#coding=utf-8
import logging
import string
from PIL import Image
from einguteswerkzeug.plugins import EGWPluginFilter
from .utils import Matrix33

fmeta = {
    "name" : "emboss",
    "version" : "0.1.9",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class Emboss(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def run(self):
        return _emboss(**self._kwargs)


filter = Emboss()
assert isinstance(filter,EGWPluginFilter)

def _emboss(img):
    '''
    @效果：浮雕
    @param img: instance of Image
    @return: instance of Image

    @不推荐使用，PIL已经内置浮雕的滤镜处理
    '''

    # 要进行卷积转换的3×3矩阵
    matrix33 = [[-1, 0, -1],
                [0, 4, 0],
                [-1, 0, -1]]
    m = Matrix33(matrix33, offset=127)
    return m.convolute(img) # 进行卷积转换
