#include <arba/vrsn/semver.hpp>
#include <arba/vrsn/version.hpp>
#include <cstdlib>
#include <iostream>

int main()
{
    vrsn::semver ver("0.1.0-dev+metadata");
    std::cout << std::format("version-{}", ver) << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
