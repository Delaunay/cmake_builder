# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'

import os
import glob
from CMBuilder.cmake_builder import CMakeBuilder

# load defaults
from CMBuilder.default_gitignore import *
from CMBuilder.utility import *
from CMBuilder.cmake import *
from CMBuilder.default_struct import *

# Overide defaults (TODO)
# OVERIDE!

configuration = ProjectConfig()
# Shortcut
conf = configuration


class CPPProject:
    source_folder_name = str()

    def __init__(self):
        self.file_config = {
            FileType.Header: '*h',
            FileType.Source: '*cpp',
            FileType.Test: '*_test.cpp'
        }

        if conf.project_folder[-1] != '/':
            self.project_path = conf.project_folder + '/' + conf.project_name + '/'
        else:
            self.project_path = conf.project_folder + conf.project_name + '/'

        self.library = []
        self.tests_files = set()

        # CMake File
        self.builder = CMakeBuilder()
        self.builder.file_config = conf.file_config
        self.builder.project_name = conf.project_name
        self.builder.project_path = self.project_path

        # if project folder does not exist create it
        if not os.path.exists(self.project_path):
            os.mkdir(self.project_path)

        self.cmake = {
            'root': open(self.project_path + 'CMakeLists.txt', 'w'),
        }

        self.root().write(self.builder.cmake_head() + "\n")

        self.create_folder_struct()

        self.add_gitignore()
        self.add_readme()

        self.write_src()
        self.write_tests()

    def create_folder_struct(self):
        # create a each defined folder
        for i in conf.folder_struct:
            if not os.path.exists(self.project_path + i):
                os.mkdir(self.project_path + i)

            if conf.folder_struct[i] == FolderTypes.Tests:
                self.builder.test_source = self.project_path + i
                self.cmake['tests'] = open(self.project_path + i + '/CMakeLists.txt', 'w')
                self.root().write(self.builder.add_subdir(i))
                # src and hds found will be compiled into 'tests_utils' library
                src, hds, tests = file_seeker(self.project_path + i, source=self.ext_src(), header=self.ext_hds(),
                                                                     test=self.ext_test())
            elif conf.folder_struct[i] == FolderTypes.Library:
                self.builder.code_source = self.project_path + i
                self.cmake['src'] = open(self.project_path + i + '/CMakeLists.txt', 'w')
                self.source_folder_name = i
                self.root().write(self.builder.add_subdir(i))

                src, hds, tests = file_seeker(self.project_path + i, source=self.ext_src(), header=self.ext_hds(), test=self.ext_test())

                lib = Library()
                lib.name = i.split('/')[-1]     # explode url and use last folder as library name
                lib.path = self.project_path + i
                lib.source_files = src
                lib.header_files = hds
                lib.tests_files = test

            elif conf.folder_struct[i] == FolderTypes.Doxygen:
                self.builder.doc_source = self.project_path + i

    def write_tests(self):
        self.tests().write(self.builder.include('../' + self.source_folder_name))
        self.tests().write(self.builder.config_test(conf.gtest_dir, 'tests/', conf.project_name))

    def write_src(self):
        # include header
        # header are mixed with source by default
        self.src().write(self.builder.include('.') + '\n')
        # add everything as library source except file defined as mains
        self.src().write(self.builder.hadcore_folder('src/', conf.project_name.upper() + '_SRC',
                                                             conf.project_name.upper() + '_HDS',
                                                     {i for i in conf.mains}) + "\n\n")

        self.src().write(self.builder.add_library(conf.project_name, [conf.project_name.upper() + '_SRC',
                                                                conf.project_name.upper() + '_HDS']) + '\n')

        self.src().write(self.builder.add_mains(conf.mains, [conf.project_name]))

    def add_gitignore(self):
        # create gitignore
        if not os.path.exists(self.project_path + '.gitignore'):
            git_ignore_f = open(self.project_path + '.gitignore', 'a')
            git_ignore_f.write(default_gitignore)

            # add specified rule
            if 'add' in conf.git_ignore:
                for i in conf.git_ignore['add']:
                    git_ignore_f.write(i + '\n')

            git_ignore_f.close()

    def add_readme(self):
        if not os.path.exists(self.project_path + 'README.md'):
            readme = open(self.project_path + 'README.md', 'a')
            readme.write(conf.project_name + '\n' + '=' * len(conf.project_name))
            readme.close()

    def add_cmakelists(self):
        src_subdir = glob.glob(self.project_path + 'src/*')
        src_subdir_final = []

        for i in src_subdir:
            if i[1:].find('.') == -1 and i[1:].find('main') == -1:
                src_subdir_final.append(i + '/')

                # add CMakeLists.txt
                tf = open(i + '/CMakeLists.txt', 'w')
                tf.close()

    def root(self):
        return self.cmake['root']

    def tests(self):
        return self.cmake['tests']

    def main(self):
        return self.cmake['main']

    def src(self):
        return self.cmake['src']

    def __delete__(self, instance):
        instance.cmake['root'].close()
        instance.cmake['src'].close()
        instance.cmake['test'].close()

    def ext_hds(self):
        return self.file_config[FileType.Header]

    def ext_src(self):
        return self.file_config[FileType.Source]

    def ext_test(self):
        return self.file_config[FileType.Test]

