import magic
import mimetypes

def get_info(file_paths):

    infos = {}

    for file_path in file_paths:

        info = {}
        typ, enc = mimetypes.guess_type(file_path)
        mgc = magic.from_file(file_path, mime=True)
        info['mime'] = typ
        info['magic'] = mgc
        print(info)
        infos[file_path] = info

    return infos
