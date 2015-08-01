# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'

from project_struct import *
from CMBuilder.project import CPPProject

project = CPPProject(project_folder, project_name)

# Check if testing info has been provided
if 'tests' in folder_struct or FileType.Test in file_config:
    project.testing = True


