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
    "name" : "nlines",
    "version" : "0.1.6",
    "description" : "a generator plotting n lines shaped by custom randomness",
    "author" : "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
}

class NLines(EGWPluginGenerator):
    def __init__(self, **kwargs):
        super().__init__(**meta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        self.add_plugin_kwargs = {  'nr_lines' : random.randint(3,800/20),
                                    'thickness' : random.randint(1, 800/100),
                                    'x_step' : random.randint(1,800/8),
                                    'img_mode' : 'RGBA',
                                    'color' : (random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(200,255)),
                                    'bg_color' : None, # if None then the generator chooses the complementary color to color for this
                                    'draw_baseline' : False,
                                 }
        self._define_mandatory_kwargs(self, **self.add_plugin_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _generate_nlines(**self.kwargs)


generator = NLines()
assert isinstance(generator,EGWPluginGenerator)


# --- .. here comes the plugin-specific part to get some work done...

# --- find complement color helpers
# https://stackoverflow.com/questions/40233986/python-is-there-a-function-or-formula-to-find-the-complementary-colour-of-a-rgb

# Sum of the min & max of (a, b, c)
def _hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def _complement(r, g, b):
    k = _hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))
# --- END find complement color

# --- producing some random values in a given range
def _random_value(x = None, min=0, max=10):
    """
    (not very eye pleasing ;)
    returns a random int between min and max
    """
    return random.randint(min,max)

def _custom_random(x = None, min=0, max=10, power=5):
    """
    isn't quite as random as random (a bit more pleasing to the eye than random)
    returns a random in between min and max
    """
    res = 1 - (random.random()**power)
    #btw. if we would raises the random number to 2 (square) the value tend to be more to 0
    #     if we would raise to the power of half the number would turn mor towards 1
    res = min + ((max - min)/ 1) * res
    return res

def _sine_stuff(x,min,max):
    res = min + ((max - min)/ 1) * math.sin(x)
    return abs(res)
# ---

# here we go
def _generate_nlines( nr_lines = 10, thickness = 3, x_step = 10,
                      img_mode = 'RGBA', color = (0,0,0,255),
                      bg_color = None, draw_baseline = True,
                      seed = None, size=(800,800) ):

    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)

    if not isinstance(color, tuple):
        color = tuple(color)
    complement_color = _complement(color[0], color[1], color[2])
    if img_mode == 'RGBA':
        complement_color = (complement_color[0],complement_color[1],complement_color[2],255)
    if not bg_color:
        log.debug("setting bg_color to complement of {}: {}".format(color,complement_color))
        bg_color = complement_color
    if not isinstance(bg_color, tuple):
        bg_color = tuple(bg_color)
    img = Image.new(img_mode, size, bg_color)
    margin = int(size[0] * 0.10)
    max_line_height = int ((size[1] - margin*2)/ nr_lines)
    max_line_length = int(size[0] - margin*2)
    log.info("nr_lines: {} x_step: {} thickness: {} margin: {}".format(nr_lines, x_step, thickness, margin))
    log.info("color: {} bg_color: {}".format(color, bg_color))
    log.debug("max_line_height: {} max_line_length: {}".format(max_line_height, max_line_length,))
    if max_line_length % x_step != 0:
        while max_line_length % x_step != 0:
            x_step -= 1
        log.info("x_step autocorrected to: {}".format(x_step))
    draw = ImageDraw.Draw(img)
    xf = 0 + margin         # from
    yf = margin + max_line_height
    xt = size[0] - margin      # to
    yt = yf
    for i in range(nr_lines):
        if draw_baseline:
            draw.line((xf,yf, xt, yt), fill=color, width=thickness)
        last_y = yf
        last_x = xf
        for x in range(int(margin), int(margin) + max_line_length + 1, x_step):
            #print(x)
            if i % 2 == 0:
                #print(x, x_step, max_line_length)
                new_y = yf - max_line_height * 0.8 + _custom_random(x, min=0, max=max_line_height * 0.8, power=4)
                new_x = x
                draw.line((last_x, last_y, new_x, new_y ), fill=color, width=thickness)
            else:
                new_y = yf - max_line_height * 0.3 + _custom_random(x, min=0, max=max_line_height * 0.3, power=5)
                new_x = x
                draw.line((last_x, last_y, new_x, new_y ), fill=color, width=thickness)
            last_x = new_x
            last_y = new_y
        yf += max_line_height
        yt = yf
    return img


if __name__ == '__main__':
    gen = NLines()
    seed, fout = random.randrange(sys.maxsize), None
    if len(sys.argv) < 2:
        print(gen.help)
        print("usage selftest: <me> image_out [<int seed>]")
    elif len(sys.argv) < 3:
        fout = sys.argv[1]
    else:
        seed = sys.argv[2]
    log.info("seed: {}".format(seed))
    random.seed(seed)
    gen = NLines(size=(1024,1024))
    print(gen.help)
    img = gen.run()
    img.save(sys.argv[1])
