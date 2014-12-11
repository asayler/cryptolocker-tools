#!/usr/bin/env python3

import os
import sys
import mimetypes
import importlib
import pprint

_MOD_PACKAGE = "mimes"
_MOD_DEFAULT = "default"

_VERBOSE = True

_SKIP_MIMES = [None, 'application/x-info', 'application/javascript', 'text/html']

def catalog(start_path):

    start_path = os.path.abspath(start_path)

    types = {}

    for root, dirs, files in os.walk(start_path):

        for fle_name in files:

            fle_path = os.path.join(root, fle_name)
            typ, enc = mimetypes.guess_type(fle_name, strict=False)

            if typ in types:
                types[typ].append(fle_path)
            else:
                types[typ] = [fle_path]

    return types

def inspect(types):

    info = {}

    for typ in types:

        if typ in _SKIP_MIMES:
            if(_VERBOSE):
                print("Skipping {} of type {}".format(len(types[typ]), typ), file=sys.stderr)
            continue

        mod_levels = [_MOD_PACKAGE] + str(typ).lower().split('/')

        while mod_levels:
            try:
                mod_name = '.'.join(mod_levels)
                mod = importlib.import_module(mod_name)
            except ImportError:
                if(_VERBOSE):
                    print("No module '{}' to inspect '{}'".format(mod_name, typ), file=sys.stderr)
                mod_levels.pop()
            else:
                if(_VERBOSE):
                    print("Using module '{}' to inspect {} '{}'".format(mod_name, len(types[typ]), typ),
                          file=sys.stderr)
                info.update(mod.get_info(types[typ]))
                break

    return info

def print_types(types):

    for typ in types:
        print("{} - {}".format(typ, len(types[typ])))

def print_encrypted(infos):

    paths = list(infos.keys())
    paths.sort()
    counts = {}

    print("\nFiles:")
    for path in paths:
        state = infos[path]['encrypted']
        if state in counts:
            counts[state] += 1
        else:
            counts[state] = 0
        print("{} - {}".format(path, state))

    print("\nEncrypted Counts:")
    for state in counts:
        print("{} - {}".format(state, counts[state]))

def copy_files(infos, enc_state, dest):

    paths = list(infos.keys())
    paths.sort()

    for path in paths:
        print("Copying {}".format(path))

if __name__ == "__main__":

    types = catalog(sys.argv[1])
    print_types(types)
    infos = inspect(types)
    print_encrypted(infos)
