# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'

from CMBuilder.Types import *


project_name = 'project_test'       # name of the project and name of the root folder
project_folder = '.'                # path were the root folder will be created
gtest_dir = '/home/midgard/Dropbox/project/gtest/gtest/'            # where gtest source is located

# How your project is organized
folder_struct = {
    'tests': FolderTypes.Tests,       # each source file in this folder will be added as a CMake test
    'src': FolderTypes.Library,       # all source file will be compiled inside a library name 'project_name'
    'doc': FolderTypes.Doxygen,
    'build': FolderTypes.Build,
    'data': FolderTypes.Data
}

# mains function
# by default main will be linked with the library defined library (src)
# src/main.cpp is implicit
mains = {'main.cpp': {}}

# glob search pattern
# file config
file_config = {
    FileType.Header: '*.h',
    FileType.Source: '*.cpp',
    FileType.Test: '*_test.cpp'
}

# add definition to the default gitignore
git_ignore = {
    'add': ['/build/']
}
