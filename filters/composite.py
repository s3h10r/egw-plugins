#!/usr/bin/env python
#coding=utf-8
"""
based on
https://stackoverflow.com/questions/29106702/blend-overlapping-images-in-python
https://stackoverflow.com/questions/3374878/with-the-python-imaging-library-pil-how-does-one-compose-an-image-with-an-alp
"""
import logging
import string
from PIL import Image
from einguteswerkzeug.helpers.gfx import crop_image_to_square, scale_square_image
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
    "name" : "composite",
    "version" : "0.1.3",
    "description" : "blend N overlapping images",
    "author" : "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
}

class Composite(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'alpha' : 0.5, 'use_sigmoid' : False }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _do_some_work(**self._kwargs)


filter = Composite()
assert isinstance(filter,EGWPluginFilter)


def _do_some_work(image,alpha=0.5,use_sigmoid=False):
    if use_sigmoid:
        log.critical("filter-plugin '%s' arg 'use_sigmoid' is not implemented yet. does nothing." % name)

    result = crop_image_to_square(image[0])
    for img in image:
        # make sure images have equal size (take the first one as reference to risize if not)
        if img.size[0] != result.size[0] or img.size[1] != result.size[1]:
            img = crop_image_to_square(img)
            img = scale_square_image(img, size = result.size[0])
        # RGBA-mode only
        #img.put_alpha(alpha) # make sure image has an alpha channel
        #result = Image.alpha_composite(result, img)
        # without RGBA:
        result = Image.blend(result, img, alpha=alpha)
    return result
