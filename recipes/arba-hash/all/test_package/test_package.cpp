#include <arba/hash/murmur_hash_2.hpp>
#include <arba/hash/version.hpp>

#include <cstdlib>
#include <iostream>

int main()
{
    std::cout << arba::hash::murmur_hash_2_u64("hello world", cppx::endianness_specific) << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
