#!/usr/bin/env python3

import os
import sys
import mimetypes
import importlib

_MIME_MODULES = "mimes"

def catalog(start_path):

    start_path = os.path.abspath(start_path)

    types = {}

    for root, dirs, files in os.walk(start_path):

        for fle_name in files:

            fle_path = os.path.join(root, fle_name)
            typ, enc = mimetypes.guess_type(fle_name)

            if typ in types:
                types[typ].append(fle_name)
            else:
                types[typ] = [fle_name]

    return types

def inspect(types):

    info = {}

    for typ in types:

        mod_name = "{}.{}".format(_MIME_MODULES, str(typ).lower().replace('/', '.'))

        try:
            mod = importlib.import_module(mod_name)
            info.update(mod.get_info(types[typ]))
        except ImportError:
            print("No module '{}' to inspect '{}'".format(mod_name, typ))

    return info

if __name__ == "__main__":

    types = catalog(sys.argv[1])
    print(types)
    infos = inspect(types)
    print(infos)
