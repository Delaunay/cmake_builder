#include "math.h"


MyMathClass::MyMathClass(int& a, int& b):
    a(a), b(b)
{}
         
int MyMathClass::add()
{
    return a + b; 
}
