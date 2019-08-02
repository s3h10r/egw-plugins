#!/usr/bin/env python
#coding=utf-8
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
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
    "name" : "oil2",
    "version" : "0.2.1",
    "description" : "",
    "author" : "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
}

class Oil2(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'brush_size' : 6, 'roughness' : 200,}
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def _generate_image(self):
        return _oil_painting(**self._kwargs)


filter = Oil2()
assert isinstance(filter,EGWPluginFilter)


def _oil_painting(image, brush_size = 6, roughness = 200):
    '''
    @效果：油画
    @param image: instance of Image
    @param brush_size: 笔刷大小，实际上为对当前像素点进行计算的范围 ，大小范围：[1, 8]
    @param roughness: 粗糙值，大小范围：[1, 255]
    @return: instance of Image

    @注意：达到和oil_painting.py几乎一致的效果
    @计算时间更长，主要目标是用更加简洁且Pythonic的代码方法书写
    '''
    if brush_size < 1: brush_size = 1
    if brush_size > 8: brush_size = 8
    if roughness < 1: roughness = 1
    if roughness > 255: roughness = 255
    width, height = image.size

    def L(p):
        '''
        @计算某个像素点p的灰度值
        @为了加快计算速度，没有再用image.convert('L')生成一个灰度图
        '''
        l = p[0] * 299/1000 + p[1] * 587/1000 + p[2] * 114/1000
        return int(l)

    if image.mode != "RGBA":
        image = image.convert("RGBA")
    dst_image = Image.new("RGBA", (width, height)) # 目标图片

    pix = image.load()
    dst_pix = dst_image.load()

    # 主计算过程
    # 计算当前像素点的brush_size宽度范围内
    # (灰度值 * 粗糙度 / 255)出现最多的像素点
    # 并计算出这些像素点的A, R, G, B平均值值
    # 以达到油画效果
    for w in range(width):
        left = max(w - brush_size, 0)
        right = min(w + brush_size, width - 1)

        for h in range(height):
            top = max(h - brush_size, 0)
            bottom = min(h + brush_size, height - 1)

            intensity = lambda p: int(L(p) * roughness / 255)
            iter = _groupby(
                           (pix[i, j] for j in range(top, bottom+1) for i in range(left, right+1)),
                           intensity
                           )
            result = max((g for g in list(iter.values())), key=len)
            RGBA = [int(sum(l) / len(l)) for l in zip(*result)]

            dst_pix[w, h] = tuple(RGBA)

    return dst_image

def _groupby(iterable, func):
    '''
    @对可迭代对象iterable里的每个元素item进行func(item)的操作
    @返回值字典
    @它将值相同的对象的值作为字典的键，将相同的对象以list的形式作为值
    @param iterable：可迭代对象
    @param func：计算函数
    '''
    results = {}
    for item in iterable:
        result = func(item)
        if result in results:
            results[result].append(item)
        else:
            results[result] = [item, ]
    return results

if __name__ == "__main__":
    print(get_plugin_doc)
    #start = time.time()
    #end = time.time()
    #print('It all spends %f seconds time' % (end-start))
