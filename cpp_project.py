# -*- coding: utf-8 -*-
__author__ = 'Pierre Delaunay'

from CMBuilder.project import CPPProject, configuration

# get args
import sys
args = sys.argv


# Read project name
if len(args) > 1:

    configuration.project_name = sys.argv[1]

    # Create the project
    CPPProject()
