#!/usr/bin/env python3
#coding=utf-8
"""
base-classes of all filters and generators
"""
from abc import ABC, abstractmethod
import logging
import string
from PIL import Image

class EGWPluginBase(ABC):
    """
    abstract base class of all plugins for einguteswerkzeug
    """
    def __init__(self, name = None, version = None, description=None, author= None):
        self._PLUGIN_IFACE_VERSION = "0.2.0"
        self._kwargs = {}
        self._name = name
        self._author = author
        self._description = description
        self._version = version
        super().__init__()


    @property
    def iface_version(self):
        """
        returns plugin interface version
        """
        return self._PLUGIN_IFACE_VERSION


    @property
    def name(self):
        return self._name


    @property
    def version(self):
        return self._version


    @property
    def author(self):
        return self._author


    def _define_mandatory_kwargs(self, *args, **kwargs):
        """
        should be used in every subclasses __init__-function to define
        (the additional) mandatory kwargs.
        """
        for k,v in kwargs.items():
            if not k in self._kwargs:
                self._kwargs[k] = v
            else: # kwargs are inherited and must be unique therefore
                raise Exception("kwarg '{}' is not unique.".format(k))


    @property #getter
    def kwargs(self):
        """
        get plugin's kwargs
        """
        return self._kwargs


    @kwargs.setter
    def kwargs(self, kwargs):
        """
        sets / modifies plugin specific kwargs
        """

        for k,v in kwargs.items():
            # btw. we can't just do self._kwargs = kwargs because we want to preserve
            # inherited args in subclasses
            if k not in kwargs: # check if we know the given kwarg
                raise Exception("Unknown kwarg {}".fortmat(k))
            self._kwargs[k] = v

    @property
    def help(self):
        """
        shows infos about the plugin, expecially the mandatory kwargs to set.
        """
        tpl_doc = string.Template("""
        $name - $description
        version : $version (plugin_iface_version : $plugin_iface_version)
        author  : $author
        kwargs  : $kwargs
        """)
        return tpl_doc.substitute({
            'name' : str(type(self)) + " " + self._name,
            'description' : self._description,
            'kwargs' : self._kwargs,
            'author'  : self._author,
            'version' : self._version,
            'plugin_iface_version' : self._PLUGIN_IFACE_VERSION
            })


        def _check_if_okay_to_run(self, null_value_allowed=False):
            """
            """
            if null_value_allowed:
                return True
            for k,v in self._kwargs.items():
                if not v:
                    raise Exception("Sorry, mandatory argument '{}' not set.".format(k))
            return True

        @abstractmethod
        def run(self):
            self._check_if_okay_to_run()
            # do the work ...
            pass


        def execute(self):
            # just an alias for run
            return self.run(self)

class EGWPluginFilter(EGWPluginBase):
    """
    base-class of a filter-plugin for einguteswerkzeug
    """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        # defining additional mandatory kwargs
        add_kwargs = {'image' : None }
        self._define_mandatory_kwargs(self, **add_kwargs)
        if 'image' in kwargs:
            self._kwargs['image'] = kwargs['image']


    @abstractmethod
    def run(self): # implement this in the subclass
        """
        returns an Image instance
        """
        if self._check_if_okay_to_run():
            return self._do_some_work(self._kwargs)


    def execute(self):
        self.run(self)


    def _do_some_work(self, **kwargs):
        raise Exception("Overwrite me in the subclass.")


class EGWPluginGenerator(EGWPluginBase):
    """
    base-class of a generator-plugin for einguteswerkzeug
    """
    def __init__(self, name, version, description = None, author = None):
        super().__init__(name, description, author, version)
        # defining additional mandatory kwargs
        add_kwargs = {'size' : (800,800) } # defines the image's output size
        self._define_mandatory_kwargs(self, **add_kwargs)


    @abstractmethod
    def run(self): # implement this in the subclass
        if self._check_if_okay_to_run():
            return self._do_some_work(self._kwargs)


    def execute(self):
        self.run(self)


    def _do_some_work(self, **kwargs): # implement this
        raise Exception("This is an example. Override me in subclass")


if __name__ == '__main__':
    # some basic selftest
    from filters.pixelsort import Pixelsort
    filter = Pixelsort()
    print(filter.help)
    filter = Pixelsort(algo=1)
    print(filter.help)
    print(type(filter))
