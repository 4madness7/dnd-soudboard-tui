import os, shutil
from consts import MEDIA_PATH

def copy_file(full_path: str) -> tuple[bool, str]:
    filename = os.path.split(full_path)[-1]
    full_media_path = os.path.join(MEDIA_PATH, filename)
    relative_media_path = f".{os.sep}" + f"{os.sep}".join(full_media_path.split(os.sep)[-2:])
    if not os.path.exists(full_media_path):
        shutil.copyfile(full_path, full_media_path,follow_symlinks=False)
        # successful copy
        return (True, relative_media_path)

    # unsuccessful copy
    return (False, relative_media_path)
