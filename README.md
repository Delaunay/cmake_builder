CMBuilder
=========

Very basic script to simplify the creation of a new cpp project.
It is not meant to replace CMake only to provide a basic CMake setup for new projects
Script currently not very flexible (lot of hardcoded things)

Directory creation with basic CMake config
* config testing using gtest
* Sources are built as lib


Usage:
------



TODO:
-----

* Beautify
* add Sphinx and doxy build inside cmake


Reddit Message:
---------------

Everybody seems to agree that CMake and its competitors are far from being ideal.
While a lot of programs exist to help you manage dependencies and help you compile
your C++ projects they are not that simple to use.

Instead of building yet another CMake competitors that will end up being as unhelpful
I propose to build a CMake Generator that will generate a Simple CMake setup given a generic
CMake structure.

I already started to build a Simple script to do that. (It is currently quite ugly since I did not have
a clear idea of what I wanted to do, you can see my ugly script [here][1]).

You can see the project setup resulting from the script [here][2]

I would like to know if you had suggestion on what the script features should be or design


[1]: link
[2]: project_setup