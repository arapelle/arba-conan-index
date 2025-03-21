#include <arba/math/vec2.hpp>
#include <arba/math/version.hpp>

#include <iostream>

int main()
{
    arba::math::vec2<int> vec(32, 42);
    vec *= 2;
    vec += math::vec2<int>(0, 4);
    std::cout << vec << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
