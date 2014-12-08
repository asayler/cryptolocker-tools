#!/usr/bin/env python3

import os
import sys
import mimetypes

_MIME_MV = ["audio/flac"]
_MIME_RM = ["image/jpeg"]

def catalog(start_path):

    start_path = os.path.abspath(start_path)

    types = {}

    for root, dirs, files in os.walk(start_path):

        for fle_name in files:

            fle_path = os.path.join(root, fle_name)
            typ, enc = mimetypes.guess_type(fle_name)
            print("{}, {}".format(fle_path, typ))

            if typ in types:
                types[typ].append(fle_name)
            else:
                types[typ] = [fle_name]

    return types

def inspect(types):

    file_info = {}

    return file_info

if __name__ == "__main__":

    types = catalog(sys.argv[1])
    print(types)
