#!/usr/bin/env python
#coding=utf-8
from io import BytesIO
import json
import logging
import math
import random
import string
import sys

from PIL import Image, ImageDraw
from geopatterns import GeoPattern
import cairosvg
from einguteswerkzeug.plugins import EGWPluginGenerator


# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
if log.hasHandlers():
    log.handlers.clear()
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate=False
# ---

meta = {
    "name" : "geopatterns",
    "version" : "0.0.1",
    "description" : "generates beautiful geometric patterns. Based on Jason Long's lovely geo_pattern Ruby-library.",
    "author" : "Python port of geopatterns by Bryan Veloso: https://github.com/bryanveloso/geopatterns"
}

class GeoPatterns(EGWPluginGenerator):
    def __init__(self, **kwargs):
        super().__init__(**meta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        types_avail=['hexagons', 'overlapping_circles', 'overlapping_rings', 'plaid', 'plus_signs', 'rings', 'sinewaves', 'squares', 'triangles', 'xes']
        self.add_plugin_kwargs = {  'pattern_type' : types_avail[random.randint(0,len(types_avail)-1)],
                                    'seed' : None
                                 }
        self._define_mandatory_kwargs(self, **self.add_plugin_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _generate_geopatterns(**self.kwargs)


generator = GeoPatterns()
assert isinstance(generator,EGWPluginGenerator)


# --- .. here comes the plugin-specific part to get some work done...


# here we go
def _generate_geopatterns( pattern_type = 'xes', seed = None, size=(800,800) ):
    if not seed:
        seed = random.randrange(sys.maxsize)
    log.info("seed: {}".format(seed))
    random.seed(seed)
    seed_string = str(seed)

    pattern = GeoPattern(seed_string, generator=pattern_type)
    png = cairosvg.svg2png(bytestring=pattern.svg_string, scale=16)
    img = Image.open(BytesIO(png))

    return img


if __name__ == '__main__':
    gen = GeoPatterns()
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
    gen = GeoPatterns(size=(1024,1024))
    print(gen.help)
    img = gen.run()
    img.save(sys.argv[1])
