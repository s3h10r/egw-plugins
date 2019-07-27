#!/usr/bin/env python
#coding=utf-8

# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "oil"
description = "a filter."
kwargs = {'image' : '<instance of PIL Image>',
          'brush_size' : 6,
          'roughness' : 200,}
args = None
author = "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
version = "0.2.0"

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(image, brush_size = 6, roughness = 200):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    return _oil_painting(image, brush_size, roughness)

# --- END all einguteswerkzeug-plugins (generators, filters) must implement this

def get_plugin_doc(format='text'):
    """
    """
    if format not in ('txt', 'text', 'plaintext'):
        raise Exception("Sorry. format %s not available. Valid options are ['text']" % format)
    tpl_doc = string.Template("""
    filters.$name - $description
    kwargs  : $kwargs
    args    : $args
    author  : $author
    version : __version__
    """)
    return tpl_doc.substitute({
        'name' : name,
        'description' : description,
        'kwargs' : kwargs,
        'args'    : args,
        'author'  : author,
        'version' : __version__,
        })
# === END einguteswerkzeug plugin-interface ===

from PIL import Image

def _oil_painting(img, brush_size = 6, roughness = 200):
    '''
    @效果：油画
    @param img: instance of Image
    @param brush_size: 笔刷大小，实际上为对当前像素点进行计算的范围 ，大小范围：[1, 8]
    @param roughness: 粗糙值，大小范围：[1, 255]
    @return: instance of Image

    @注意：此方法速度较慢
    '''

    if brush_size < 1: brush_size = 1
    if brush_size > 8: brush_size = 8

    if roughness < 1: roughness = 1
    if roughness > 255: roughness = 255

    width, height = img.size

    gray_img = img.convert("L") # 进行灰度预处理
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    dst_img = Image.new("RGBA", (width, height)) # 目标图片

    gray_pix = gray_img.load()
    pix = img.load()
    dst_pix = dst_img.load()

    arr_len = roughness + 1
    count = [0 for i in range(arr_len)]
    A = [0 for i in range(arr_len)]
    R = [0 for i in range(arr_len)]
    G = [0 for i in range(arr_len)]
    B = [0 for i in range(arr_len)]

    def reset():
        # 将count, A, R, G, B元素重置0
        for arr in (count, A, R, G, B):
            for i in range(arr_len):
                arr[i] = 0

    # 主计算过程
    # 计算当前像素点的brush_size宽度范围内
    # (灰度值 * 粗糙度 / 255)出现最多的像素点
    # 并计算出这些像素点的A, R, G, B平均值值
    # 以达到油画效果
    for w in range(width):
        left = w - brush_size
        if left < 0:
            left = 0

        right = w + brush_size
        if right > width - 1:
            right = width - 1

        for h in range(height):
            top = h - brush_size
            if top < 0:
                top = 0

            bottom = h + brush_size
            if bottom > height - 1:
                bottom = height - 1

            reset()

            for i in range(left, right+1):
                for j in range(top, bottom+1):
                    intensity = int(gray_pix[i, j] * roughness / 255)
                    count[intensity] += 1
                    p = pix[i, j]
                    A[intensity] += p[3]
                    R[intensity] += p[0]
                    G[intensity] += p[1]
                    B[intensity] += p[2]

            max_ins_count = max(count)
            max_idx = count.index(max_ins_count)

            dst_pix[w, h] = int(R[max_idx] / max_ins_count), \
                            int(G[max_idx] / max_ins_count), \
                            int(B[max_idx] / max_ins_count), \
                            int(A[max_idx] / max_ins_count)

    return dst_img

if __name__ == "__main__":
    print(get_plugin_doc)
    #start = time.time()
    #end = time.time()
    #print('It all spends %f seconds time' % (end-start))
