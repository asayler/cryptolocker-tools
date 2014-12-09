#!/usr/bin/env python3

import os
import sys
import mimetypes
import importlib
import pprint

_MOD_PACKAGE = "mimes"
_MOD_DEFAULT = "default"

def catalog(start_path):

    start_path = os.path.abspath(start_path)

    types = {}

    for root, dirs, files in os.walk(start_path):

        for fle_name in files:

            fle_path = os.path.join(root, fle_name)
            typ, enc = mimetypes.guess_type(fle_name)

            if typ in types:
                types[typ].append(fle_path)
            else:
                types[typ] = [fle_path]

    return types

def inspect(types):

    info = {}

    for typ in types:

        mod_levels = [_MOD_PACKAGE] + str(typ).lower().split('/')

        while mod_levels:
            try:
                mod_name = '.'.join(mod_levels)
                mod = importlib.import_module(mod_name)
            except ImportError:
                print("No module '{}' to inspect '{}'".format(mod_name, typ))
                mod_levels.pop()
            else:
                info.update(mod.get_info(types[typ]))
                break

    return info

if __name__ == "__main__":

    types = catalog(sys.argv[1])
    infos = inspect(types)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(infos)
