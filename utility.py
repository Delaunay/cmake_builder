# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'

#   Quick and dirty utilities
#       file name will not have more than one '.'
#       file has an extension
#       folder name will never have one or more '.'
import glob


def glob_clean_path(path, pattern, folder=''):
    # delete the path to return only folder/file_name
    # replace '\' by '/' for windows
    ret = glob.glob(path + folder + pattern)
    return [i.replace('\\', '/').replace(path, '') for i in ret]


def glob_folder(path, pattern, folder=''):
    # if a file does not have an extension it will be considered as a folder =S
    return [i for i in filter(lambda x: x.find('.') == -1, glob_clean_path(path, pattern, folder))]


def glob_file(path, pattern, folder=''):
    # assume a file will have an extension
    return [i for i in filter(lambda x: x.find('.') != -1, glob_clean_path(path, pattern, folder))]


def glob_recursive(path, pattern, folder=''):

    fold_ = glob_folder(path, '*', folder)      # <= we want all the folder
    file_ = glob_file(path, pattern, folder)    # <= we want only file matching pattern

    for i in fold_:
        fo, fi = glob_recursive(path + folder, pattern, i + '/')

        fold_ += fo
        file_ += fi

    return fold_, file_