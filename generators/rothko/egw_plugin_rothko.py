#!/usr/bin/env python
#coding=utf-8
import logging
import json
import math
import random
import string
import sys

from PIL import Image, ImageDraw
from einguteswerkzeug.plugins import EGWPluginGenerator

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

meta = {
    "name" : "rothko",
    "version" : "0.1.0",
    "description" : "adaption of [RothkoBot](https://github.com/ZacharyDavis/RothkoBot), Copyright (c) 2017 Zachary Davis",
}

class Rothko(EGWPluginGenerator):
    def __init__(self, **kwargs):
        super().__init__(**meta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        self.add_plugin_kwargs = {
                                    'seed' : None
                                 }
        self._define_mandatory_kwargs(self, **self.add_plugin_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _do_rothko(**self.kwargs)


generator = Rothko()
assert isinstance(generator,EGWPluginGenerator)


# --- .. here comes the plugin-specific part to get some work done...


# here we go
def _do_rothko(color_file='colors.txt', seed = None, size=(418,518), \
               img_mode='RGBA', bg_color = (255,255,255,255)):
    if not seed:
        seed = random.randrange(sys.maxsize)
    log.info("seed: {}".format(seed))
    random.seed(seed)
    if not bg_color or not isinstance(bg_color,tuple) or len(bg_color) !=4:
        bg_color = (255,255,255,255)
    img = Image.new(img_mode, size, bg_color)
    draw = ImageDraw.Draw(img)

    # read colornames and rgb-string from file
    f_in = open(color_file, "r")
    colors = f_in.read().splitlines()
    f_in.close()
    four_colors = False
    color1 = colors[random.randint(0,len(colors)-1)].split(",")  # background color and name
    color2 = colors[random.randint(0,len(colors)-1)].split(",")  # first rectangle color and name
    color3 = colors[random.randint(0,len(colors)-1)].split(",")  # second rectangle color and name
    color4 = colors[random.randint(0,len(colors)-1)].split(",")  # third rectangle color and name
    # decode hex color values to (R,G,B) format
    color_str1 = tuple(int(color1[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    color_str2 = tuple(int(color2[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    color_str3 = tuple(int(color3[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    color_str4 = tuple(int(color4[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    log.info("color1 {} = {}".format(color1,color_str1))
    log.info("color2 {} = {}".format(color2,color_str2))
    log.info("color3 {} = {}".format(color3,color_str3))
    log.info("color4 {} = {}".format(color4,color_str4))

    w,h = size[0],size[1]
    length1 = random.randint(math.floor((h / 100) * 1.94),math.floor((h / 100) * 54.0))  # Determine lengths of each rectangle
    length2 = random.randint(0,(math.floor((h / 100) * 92.8)-length1))
    length3 = math.floor((h / 100) * 89.4)-(length2+length1)
    draw.rectangle([0, 0, w, h], fill=color_str1, outline=color_str1)
    draw.rectangle([math.floor((h / 100) * 3.9),math.floor((h / 100) * 3.9), w-math.floor((h / 100) * 3.9), length1+math.floor((h / 100) * 3.9)], fill=color_str2, outline=color_str2)
    draw.rectangle([math.floor((h / 100) * 3.9), length1+math.floor((h / 100) * 5.9), w-math.floor((h / 100) * 3.9), length2+length1+math.floor((h / 100) * 5.9)], fill=color_str3, outline=color_str3)
    if length3 > 0:
        draw.rectangle([math.floor((h / 100) * 3.9), length1+length2+math.floor((h / 100) * 7.9), w-math.floor((h / 100) * 3.9), length1+length2+length3+math.floor((h / 100) * 7.9)], fill=color_str4, outline=color_str4)
        four_colors = True
    if four_colors:
        sTitle = "No. " + str(seed) + " (" + color2[0].title() + ", " + color3[0].title() + ", and " + color4[0].title() + " on " + color1[0].title() + ")"
    else:
        sTitle = "No. " + str(seed) + " (" + color2[0].title() + " and " + color3[0].title() + " on " + color1[0].title() + ")"
    log.info("sTitle:{}".format(sTitle))
    return img


if __name__ == '__main__':
    gen = Rothko()
    seed, fout = random.randrange(sys.maxsize), None
    if len(sys.argv) < 2:
        print(gen.help)
        print("usage selftest: <me> image_out [<int seed>]")
        sys.exit(0)
    elif len(sys.argv) < 3:
        fout = sys.argv[1]
    else:
        seed = sys.argv[2]
    log.info("seed: {}".format(seed))
    random.seed(seed)
    #gen = Rothko(size=(418,518),seed=seed)
    gen = Rothko(size=(600,600),seed=seed)
    print(gen.help)
    img = gen.run()
    img.save(sys.argv[1])
