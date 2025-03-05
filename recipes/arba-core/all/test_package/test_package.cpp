#include <arba/core/string/trim.hpp>
#include <arba/core/version.hpp>
#include <cstdlib>
#include <iostream>

int main()
{
    std::cout << core::trim_view("  __package__  ") << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
