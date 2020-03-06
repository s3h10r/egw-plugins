#!/usr/bin/env python
#coding=utf-8
import logging
import json
import math
import os
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
    "version" : "0.1.2",
    "description" : "adaption of [RothkoBot](https://github.com/ZacharyDavis/RothkoBot), Copyright (c) 2017 Zachary Davis",
}

class Rothko(EGWPluginGenerator):
    def __init__(self, **kwargs):
        super().__init__(**meta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        self.add_plugin_kwargs = {
                                    'seed' : None,
                                    'palette' : 'colors.txt',
                                    'color1' : None,
                                    'color2' : None,
                                    'color3' : None,
                                    'color4' : None,

                                 }
        self._define_mandatory_kwargs(self, **self.add_plugin_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _do_rothko(**self.kwargs)


generator = Rothko()
assert isinstance(generator,EGWPluginGenerator)


# --- .. here comes the plugin-specific part to get some work done...


# here we go
def _do_rothko(palette='colors.txt', seed = None, size=(418,518), \
               img_mode='RGBA', color1 = None, \
               color2 = None, color3 = None, color4 = None):
    """
    color_palette:
        plaintextfile with a palette of colors as strings in the format
        described below

    color1..4:
        colors are strings in the following format: '<name>,#<rr><gg><bb>'

    example:
        color1='pebble gray,#e0e4cc'
    """

    if not seed:
        seed = random.randrange(sys.maxsize)
    log.info("seed: {}".format(seed))
    random.seed(seed)
    if color1:
        if isinstance(color1,str):
            color1 = color1.split(",")
        else:
            color1 = None
    if color2: color2 = color2.split(",")
    if color3: color3 = color3.split(",")
    if color4: color4 = color4.split(",")
    img = Image.new(img_mode, size,(255,255,255,255))
    draw = ImageDraw.Draw(img)

    # read colornames and rgb-string from file
    try:
        f_in = open(palette,'r')
    except:
        f_in = open("{}/{}".format( \
            os.path.dirname(os.path.realpath(__file__)),palette),'r')
    colors = f_in.read().splitlines()
    f_in.close()
    four_colors = False
    if not color1:
        color1 = colors[random.randint(0,len(colors)-1)].split(",")  # background color and name
    else:
        # dummy for getting same result for same seed
        random.randint(0,len(colors)-1)
    if not color2:
        color2 = colors[random.randint(0,len(colors)-1)].split(",")  # first rectangle color and name
    else:
        # dummy for getting same result for same seed
        random.randint(0,len(colors)-1)
    if not color3:
        color3 = colors[random.randint(0,len(colors)-1)].split(",")  # second rectangle color and name
    else:
        # dummy for getting same result for same seed
        random.randint(0,len(colors)-1)
    if not color4:
        color4 = colors[random.randint(0,len(colors)-1)].split(",")  # third rectangle color and name
    else:
        # dummy for getting same result for same seed
        random.randint(0,len(colors)-1)
    # decode hex color values to (R,G,B) format
    color1_rgba = tuple(int(color1[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    color2_rgba = tuple(int(color2[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    color3_rgba = tuple(int(color3[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    color4_rgba = tuple(int(color4[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    log.info("color1 {} = {}".format(color1,color1_rgba))
    log.info("color2 {} = {}".format(color2,color2_rgba))
    log.info("color3 {} = {}".format(color3,color3_rgba))
    log.info("color4 {} = {}".format(color4,color4_rgba))

    w,h = size[0],size[1]
    length1 = random.randint(math.floor((h / 100) * 1.94),math.floor((h / 100) * 54.0))  # Determine lengths of each rectangle
    length2 = random.randint(0,(math.floor((h / 100) * 92.8)-length1))
    length3 = math.floor((h / 100) * 89.4)-(length2+length1)
    draw.rectangle([0, 0, w, h], fill=color1_rgba, outline=color1_rgba)
    draw.rectangle([math.floor((h / 100) * 3.9),math.floor((h / 100) * 3.9), w-math.floor((h / 100) * 3.9), length1+math.floor((h / 100) * 3.9)], fill=color2_rgba, outline=color2_rgba)
    draw.rectangle([math.floor((h / 100) * 3.9), length1+math.floor((h / 100) * 5.9), w-math.floor((h / 100) * 3.9), length2+length1+math.floor((h / 100) * 5.9)], fill=color3_rgba, outline=color3_rgba)
    if length3 > 0:
        draw.rectangle([math.floor((h / 100) * 3.9), length1+length2+math.floor((h / 100) * 7.9), w-math.floor((h / 100) * 3.9), length1+length2+length3+math.floor((h / 100) * 7.9)], fill=color4_rgba, outline=color4_rgba)
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
