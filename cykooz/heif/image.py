# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 25.06.2019
"""
import os
from typing import Optional

from cykooz.heif.rust2py import open_heif_file, HeifImage as _RustHeifImage

from .typing import PathLike


class HeifImage:

    def __init__(self, path: PathLike):
        self._image: _RustHeifImage = open_heif_file(os.fspath(path))
        self._exif = None
        self._is_exif_loaded = False
        self._data = None
        self._stride = None
        self._bits_per_pixel = None
        self._is_data_loaded = False

    @property
    def width(self) -> int:
        return self._image.width

    @property
    def height(self) -> int:
        return self._image.height

    @property
    def mode(self) -> str:
        return self._image.mode

    @property
    def exif(self) -> Optional[bytes]:
        if not self._is_exif_loaded:
            self._exif = self._image.get_exif()
            self._is_exif_loaded = True
        return self._exif

    def _load_plane(self):
        if self._is_data_loaded:
            return
        self._data, self._stride, self._bits_per_pixel = self._image.get_data()
        self._is_data_loaded = True

    @property
    def data(self) -> Optional[bytes]:
        self._load_plane()
        return self._data

    @property
    def stride(self) -> Optional[int]:
        self._load_plane()
        return self._stride

    @property
    def bits_per_pixel(self) -> Optional[int]:
        self._load_plane()
        return self._bits_per_pixel