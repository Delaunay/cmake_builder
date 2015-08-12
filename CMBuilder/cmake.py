# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'


def add_var(var_name, value, p=''):
    s = 'SET(' + var_name + '\n'
    for i in value:
        s += '    ' + p + i + '\n'
    return s[:-1] + ')'


class Library:
    source_files = set()
    header_files = set()
    test_files = set()
    name = ''
    path = ''
    include = ''

    def header_var(self):
        return self.name.upper() + '_HEADER'

    def source_var(self):
        return self.name.upper() + '_SOURCE'

    def __str__(self):
        # ADD Source
        s  = 'INCLUDE_DIRECTORY(.)\n'
        s += add_var(self.header_var(), self.header_files) + '\n'
        s += add_var(self.source_var(), self.source_files) + '\n'
        s += add_var(self.name.upper(), ['${' + self.source_var() + '}', '${' + self.header_var() + '}']) + '\n'

        s += 'ADD_LIBRARY(' + self.name + ' ${' + self.name.upper() + '})\n'

        # add test
        return s


def test(name):
    return "   CBTEST_MACRO(" + name + ")\n"
