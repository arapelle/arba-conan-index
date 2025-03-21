#include <arba/cppx/version.hpp>
#include <arba/cppx/version/semver.hpp>

#include <cstdlib>
#include <iostream>

int main()
{
    std::cout << std::format("{}", cppx::semver("0.1.0-dev+metadata")) << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
