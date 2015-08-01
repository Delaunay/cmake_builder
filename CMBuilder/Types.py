# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'

from enum import Enum


class FolderTypes(Enum):
    Tests = 0           #
    Library = 1
    Executable = 2
    Include = 3
    Sphinx = 4
    Doxygen = 5
    Build = 6
    NewFolder = 7
    Data = 8


class FileType(Enum):
    Source = 0,
    Header = 1,
    Test = 2

