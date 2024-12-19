#include <arba/hash/murmur_hash.hpp>
#include <arba/hash/version.hpp>
#include <cstdlib>
#include <iostream>

int main()
{
    std::cout << arba::hash::neutral_murmur_hash_64("hello world") << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
