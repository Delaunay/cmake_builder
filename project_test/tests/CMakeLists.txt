INCLUDE_DIRECTORIES(../src)
OPTION(BUILD_TESTING "Enable tests" ON)
SET(gtest_dir /home/midgard/Dropbox/project/gtest/gtest/)

IF(BUILD_TESTING)
   # Compile gtest
   INCLUDE_DIRECTORIES(${gtest_dir})
   INCLUDE_DIRECTORIES(${gtest_dir}/include/)
   ADD_LIBRARY(gtest ${gtest_dir}/src/gtest-all.cc)

   # Macro
   MACRO(CBTEST_MACRO NAME)
      ADD_EXECUTABLE(${NAME}_test ${NAME}_test.cpp )
      TARGET_LINK_LIBRARIES(${NAME}_test project_test gtest -pthread)
      ADD_TEST(NAME ${NAME}_test
         COMMAND ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${NAME}_test)
   ENDMACRO(CBTEST_MACRO)

   CBTEST_MACRO(my_test)
ENDIF(BUILD_TESTING)
