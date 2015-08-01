# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'
import os
import glob
from CMBuilder.cmake_builder import CMakeBuilder

# load defaults
from CMBuilder.default_gitignore import *
from CMBuilder.default_struct import *

# Overide defaults (TODO)
# OVERIDE!


class CPPProject:

    def __init__(self):

        # CMake File
        self.builder = CMakeBuilder()
        self.builder.file_config = file_config

        if 'tests' in folder_struct or FileType.Test in file_config:
            self.testing = True
        else:
            self.testing = False

        if project_folder[-1] != '/':
            self.project_path = project_folder + '/' + project_name + '/'
        else:
            self.project_path = project_folder + project_name + '/'

        self.builder.project_name = project_name
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
        for i in folder_struct:
            if not os.path.exists(self.project_path + i):
                os.mkdir(self.project_path + i)

            if folder_struct[i] == FolderTypes.Tests:
                self.builder.test_source = self.project_path + i
                self.cmake['tests'] = open(self.project_path + i + '/CMakeLists.txt', 'w')
                self.root().write(self.builder.add_subdir(i))
            elif folder_struct[i] == FolderTypes.Library:
                self.builder.code_source = self.project_path + i
                self.cmake['src'] = open(self.project_path + i + '/CMakeLists.txt', 'w')
                self.root().write(self.builder.add_subdir(i))
            elif folder_struct[i] == FolderTypes.Doxygen:
                self.builder.doc_source = self.project_path + i

    def write_tests(self):
        self.tests().write(self.builder.include(project_name.upper() + '_HDS'))
        self.tests().write(self.builder.config_test(gtest_dir, 'tests/', project_name))

    def write_src(self):
        self.src().write(self.builder.include() + '\n')
        self.src().write(self.builder.hadcore_folder('src/', project_name.upper() + '_SRC',
                                                             project_name.upper() + '_HDS') + "\n\n")

        self.src().write(self.builder.add_library(project_name, [project_name.upper() + '_SRC',
                                                                project_name.upper() + '_HDS']) + '\n')

        self.src().write(self.builder.add_mains(mains, [project_name]))

    def add_gitignore(self):
        # create gitignore
        if not os.path.exists(self.project_path + '.gitignore'):
            git_ignore_f = open(self.project_path + '.gitignore', 'a')
            git_ignore_f.write(default_gitignore)

            # add specified rule
            if 'add' in git_ignore:
                for i in git_ignore['add']:
                    git_ignore_f.write(i + '\n')

            git_ignore_f.close()

    def add_readme(self):
        if not os.path.exists(self.project_path + 'README.md'):
            readme = open(self.project_path + 'README.md', 'a')
            readme.write(project_name + '\n' + '=' * len(project_name))
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


CPPProject()
