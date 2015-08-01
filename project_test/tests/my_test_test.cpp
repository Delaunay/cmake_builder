#ifndef VANAGANDR_TEST_EIGENDATE_HEADER
#define VANAGANDR_TEST_EIGENDATE_HEADER

#include <gtest/gtest.h>
#include "functions/my_header.h"

TEST(main_name, sub_name)
{
    print_hello_world();
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();

    return 0;
}

#endif

