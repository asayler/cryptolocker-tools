import magic
import mimetypes

_ENCODING = "utf-8"

_MGC_ENCRYPTED = 'application/octet-stream'

def get_info(file_paths):

    infos = {}

    for file_path in file_paths:

        info = {}
        typ, enc = mimetypes.guess_type(file_path)
        mgc = magic.from_file(file_path, mime=True).decode(_ENCODING)
        info['mime'] = typ
        info['magic'] = mgc
        if (mgc == _MGC_ENCRYPTED):
            if (typ == None):
                info['encrypted'] = "unknown"
            elif (typ == mgc):
                info['encrypted'] = "unknown"
            else:
                info['encrypted'] = "probably"
        else:
            info['encrypted'] = "no"
        infos[file_path] = info

    return infos
