#!/usr/bin/env python3

import os
import sys
import mimetypes
import importlib
import shutil

_MOD_PACKAGE = "mimes"
_SKIP_MIMES = [None, 'application/x-info', 'application/javascript', 'text/html']
_SKIP_NAMES = ['DECRYPT_INSTRUCTION.TXT']

_VERBOSE = True
_OVERWRITE = True

def catalog(src_root):

    types = {}

    for root, dirs, files in os.walk(src_root):

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

    if(_VERBOSE):
        print("\nInspecting Types:", file=sys.stderr)

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
                mod_levels.pop()
            else:
                if(_VERBOSE):
                    print("Using module '{}' to inspect {} of type {}".format(mod_name,
                                                                              len(types[typ]), typ),
                          file=sys.stderr)
                info.update(mod.get_info(types[typ]))
                break

    return info

def print_types(types):

    print("\nFile Type Stats:", file=sys.stderr)
    for typ in types:
        print("{} - {}".format(typ, len(types[typ])), file=sys.stderr)

def print_encrypted(infos):

    paths = list(infos.keys())
    paths.sort()
    type_counts = {}
    type_counts['Total'] = {}

    print("\nFile List:")
    for path in paths:
        state = infos[path]['encrypted']
        if state in type_counts['Total']:
            type_counts['Total'][state] += 1
        else:
            type_counts['Total'][state] = 1
        typ = infos[path]['mime']
        if typ in type_counts:
            if state in type_counts[typ]:
                type_counts[typ][state] += 1
            else:
                type_counts[typ][state] = 1
        else:
            type_counts[typ] = {}
            type_counts[typ][state] = 1
        print("{} - {}".format(path, state))

    print("\nEncryption Stats:", file=sys.stderr)
    for typ in type_counts:
        sys.stderr.write("{}: ".format(typ))
        sys.stderr.write("count = {}".format(sum(type_counts[typ].values())))
        for state in type_counts[typ]:
            sys.stderr.write(", {} = {}".format(state, type_counts[typ][state]))
        sys.stderr.write("\n")

def copy_files(infos, src_root, dst_root):

    paths = list(infos.keys())
    paths.sort()

    for src_path in paths:
        state = infos[src_path]['encrypted']
        rel_path = os.path.relpath(src_path, start=src_root)
        dst_path = os.path.join(dst_root, state, rel_path)
        dst_dir = os.path.dirname(dst_path)
        src_name = os.path.basename(src_path)
        if src_name in _SKIP_NAMES:
            print("Skipping '{}'".format(src_path), file=sys.stderr)
            continue
        else:
            print("Copying '{}' to '{}'".format(src_path, dst_path), file=sys.stderr)
        if os.path.exists(dst_path):
            if _OVERWRITE:
                print("'{}' Already Exists, Overwriting".format(dst_path), file=sys.stderr)
                os.remove(dst_path)
                shutil.copy2(src_path, dst_path)
            else:
                print("'{}' Already Exists, Skipping".format(dst_path), file=sys.stderr)
        else:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src_path, dst_path)

if __name__ == "__main__":

    src_root = os.path.abspath(sys.argv[1])
    dst_root = os.path.abspath(sys.argv[2])

    types = catalog(src_root)
    print_types(types)
    infos = inspect(types)
    print_encrypted(infos)
    copy_files(infos, src_root, dst_root)
