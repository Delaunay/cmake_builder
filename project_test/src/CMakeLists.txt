INCLUDE_DIRECTORIES(.)

SET(PROJECT_TEST_HDS
    math.h
    functions/my_header.h)

SET(PROJECT_TEST_SRC
    functions/my_source.cpp
    math.cpp)

ADD_LIBRARY(project_test ${PROJECT_TEST_SRC} ${PROJECT_TEST_HDS})

ADD_EXECUTABLE(main main.cpp)
TARGET_LINK_LIBRARIES(main project_test)

