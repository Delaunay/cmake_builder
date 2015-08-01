# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'
#
# from project_struct import *
# from CMBuilder.project import CPPProject
#
# project = CPPProject(project_folder, project_name)
#
# # Check if testing info has been provided
# if 'tests' in folder_struct or FileType.Test in file_config:
#     project.testing = True
#
#


s1 = {1, 2, 3}
s2 = {3, 4, 5}

# s1.add(4)
# s1.pop(s2)
s1 = s1.union(s2)

print(s1)