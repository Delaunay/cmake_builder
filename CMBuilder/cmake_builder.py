# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'
from utility import *
from CMBuilder.Types import *


class CMakeBuilder:
    # create a fairly standard cpp CMake file which follow a fairly standard directory setup
    #   |project_name/
    #   |||||+-----CMakeLists.txt
    #   ||||+------/src
    #   |||+-------/doc
    #   ||+--------/test
    #   |+---------/data
    #   +----------/build-release ...
    # gtest as unit testing framework
    # CMake builder build your cpp project as a library
    # your main is then build using that library
    # you can easily compile multiple main that way

    def __init__(self):
        self.file_config = {
            FileType.Header: '*h',
            FileType.Source: '*cpp',
            FileType.Test: '*_test.cpp'
        }

        self.code_source = None
        self.doc_source = None
        self.test_source = None
        self.main_folder = None
        self.project_name = ''

        # ${PROJECT_SOURCE_DIR}
        self.project_path = None
        self.library = {self.project_name.upper() + '_SRC': [], self.project_name.upper() + '_HDS': []}

        self.cmake_var = {}

    def ext_hds(self):
        return self.file_config[FileType.Header]

    def ext_src(self):
        return self.file_config[FileType.Source]

    def ext_test(self):
        return self.file_config[FileType.Test]

    def cmake_head(self, major=0, minor=0, patch=0):
        s = "PROJECT(" + self.project_name + ")\n" +\
            "CMAKE_MINIMUM_REQUIRED(VERSION 2.8.4)\n" +\
            "SET(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -std=c++11 \")\n\n" +\
            \
            "SET(CMAKE_RELEASE_POSTFIX \"\")\n" +\
            "SET(CMAKE_DEBUG_POSTFIX \"-debug\")\n" +\
            \
            "SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n" +\
            "SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)\n" +\
            "SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)\n\n" +\
            "ENABLE_TESTING()\n"

        if major != minor != patch:
            s += "SET(VERSION_MAJOR " + str(major) + ")" +\
                 "SET(VERSION_MINOR " + str(minor) + ")" +\
                 "SET(VERSION_PATCH " + str(patch) + ")" +\
                 "SET(VERSION" +\
                 "    ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH})"
        return s

    def add_cmake_folder(self, cmake_folder_path):
        return "LIST(APPEND CMAKE_MODULE_PATH " + cmake_folder_path + ")"

    # add file one by one
    def hadcore_folder(self, folder_name, var_src, var_hds=None):
        # if var_hds is set SRC and Header are separated

        if var_hds is None:
            src = glob_recursive(self.project_path + folder_name, self.ext_src())[1]
            src += glob_recursive(self.project_path + folder_name, self.ext_hds())[1]

            self.cmake_var[var_src] = 1

            return self.add_var(var_src, src)
        else:
            src = glob_recursive(self.project_path + folder_name, self.ext_src())[1]
            hds = glob_recursive(self.project_path + folder_name, self.ext_hds())[1]

            self.cmake_var[var_src] = 1
            self.cmake_var[var_hds] = 1

            return self.add_var(var_hds, hds) + '\n\n' + self.add_var(var_src, src)
            
    def include(self, var = None):
        #if var in self.cmake_var:
        #    return 'INCLUDE_DIRECTORIES(${' + var + '})\n' 
        #else:
        return 'INCLUDE_DIRECTORIES(../src/)\n' 

    # using CMake directory
    def add_src_folder(self, folder_name, var=None):
        if var is None:
            var = self.project_name.upper() + '_SRC'

        # add a folder
        # if the folder does not exist it is created and CMakeLists.txt is added ?
        s = 'AUX_SOURCE_DIRECTORY(' + folder_name + ' ' + var + ')\n' +\
            'ADD_SUBDIRECTORY(' + folder_name + ')'
        return s

    def add_var(self, varname, value, p=''):
        s = 'SET(' + varname + '\n'
        for i in value:
            if i.find('main/') == -1:
                s += '    ' + p + i + '\n'
        return s[:-1] + ')'

    def add_library(self, lib, source):
        self.library[lib] = []
        s = 'ADD_LIBRARY(' + lib + ' '
        if type(source) is str:
            s += '${' + source + '} '
        else:
            for i in source:
                s += '${' + i + '} '
        s = s[:-1] + ')\n'        
        # s += "link_directories(${PROJECT_BINARY_DIR})\n"
        return s

    def add_subdir(self, dir):
        return "ADD_SUBDIRECTORY(" + dir + ")\n"

    def config_test(self, gtest_dir, test_dir, lib):
        # gtest recommend to build gtest for each project
        s =  "OPTION(BUILD_TESTING \"Enable tests\" ON)\n" +\
             "SET(gtest_dir " + gtest_dir + ")\n\n" +\
             "IF(BUILD_TESTING)\n"

        s += "   # Compile gtest\n" +\
             "   INCLUDE_DIRECTORIES(${gtest_dir})\n" +\
             "   INCLUDE_DIRECTORIES(${gtest_dir}/include/)\n" +\
             "   ADD_LIBRARY(gtest ${gtest_dir}/src/gtest-all.cc)\n\n"

        s += "   # Macro\n" +\
             "   MACRO(CBTEST_MACRO NAME)\n" +\
             "      ADD_EXECUTABLE(${NAME}_test " + "${NAME}" + self.ext_test()[1:] + " )\n" +\
             "      TARGET_LINK_LIBRARIES(${NAME}_test " + lib + " gtest -pthread)\n" +\
             "      ADD_TEST(NAME ${NAME}_test\n" +\
             "         COMMAND ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${NAME}_test)\n" +\
             "   ENDMACRO(CBTEST_MACRO)\n\n"

        test_files = []
        if test_dir is not None:
            test_files += glob.glob(self.project_path + test_dir + self.ext_test())

        for i in test_files:
            s += "   CBTEST_MACRO(" + i[len(self.project_path + test_dir):-9] + ")\n"

        s += "ENDIF(BUILD_TESTING)\n"
        return s

    def add_mains(self, dict_main, lib):

        s = ''

        for i in dict_main:
            # if it is a file add executable

            if i.find('.') != -1:
                s += 'ADD_EXECUTABLE(' + i[:-4] + ' ' + i + ')\n'
                s += "TARGET_LINK_LIBRARIES(" + i[:-4]

                for j in lib:
                    s += ' ' + j

                s += ')\n\n'
            else:
                s += self.add_main_folder(i, lib)

        return s

    def add_main_folder(self, folder, lib):
        
        mains = glob_file(self.project_path + 'src/main/', self.ext_src())
        s = ''
        
        for i in mains:
            s += 'ADD_EXECUTABLE(' + i[:-4] + ' ' + folder + i + ')\n'
            s += "TARGET_LINK_LIBRARIES(" + i[:-4]
            
            for j in lib:
                s += ' ' + j
            
            s += ')\n\n'
        
        return s

    def add_option(self, var, message, value):
        return "OPTION(" + var + " \"" + message + "\" " + value + ")\n"


if __name__ == '__main__':
    ss = CMakeBuilder()

    ss.project_path = 'C:/Users/pastafarian/Dropbox/project/vanagandr/'
    ss.code_source = 'src/'
    ss.test_source = 'test/'
    ss.project_name = 'vanagandr'

    # print(ss.cmake_head())
    # print(ss.config_test('', ss.test_source, ss.project_name))
    print(ss.project_path + 'src/')
    print(ss.hadcore_folder('src/', 'SRC', 'HDS'))
    # print(ss.add_src_folder('C:/Users/pastafarian/Dropbox/project/vanagandr/src/finance'))