# -*- coding:utf-8 -*-
import os
from typing import AnyStr


def try_file(path: AnyStr) -> (bool, str):
    if path.startswith('~'):
        path = os.path.expanduser(path)

    if not path.startswith('/'):
        path = os.path.abspath(path)

    existed = os.path.exists(path)
    return existed, path


def try_directory(dirname: AnyStr,
                  mkdir: bool = False) -> (bool, str):
    """ Test if given path exists and is a directory.

    Will cast given relative path to absolute path.
    """
    existed, dirname = try_file(dirname)

    if (not existed) and mkdir:
        os.mkdir(dirname)
        existed = True

    is_dir = os.path.isdir(dirname)
    ok = existed and is_dir

    return ok, dirname


FILE_TYPE_SUBTITLES = 'subtitles'
FILE_TYPE_VIDEO = 'video'
FILE_TYPE_IMAGE = 'image'
DEFAULT_FILE_TYPE = FILE_TYPE_VIDEO

EXT_MAP = {
    'srt': FILE_TYPE_SUBTITLES,
    'jpg': FILE_TYPE_IMAGE,
    'png': FILE_TYPE_IMAGE,
    'webp': FILE_TYPE_IMAGE,
    'webm': FILE_TYPE_VIDEO,
    'mp4': FILE_TYPE_VIDEO,
    '3gp': FILE_TYPE_VIDEO,
    'mov': FILE_TYPE_VIDEO,
    'avi': FILE_TYPE_VIDEO
}


def file_type_by_ext(ext: str) -> str:
    ext = ext.lower().strip()
    return EXT_MAP.get(ext, DEFAULT_FILE_TYPE)
