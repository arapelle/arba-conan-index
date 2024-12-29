#include <arba/stdx/algorithm/unstable_erase.hpp>
#include <arba/stdx/version.hpp>
#include <cstdlib>
#include <iostream>
#include <vector>

int main()
{
    std::vector<int> vec = { 0, 1, 2, 3, 4, 5, 6, 7 };
    const auto iter = vec.begin();
    stdx::unstable_erase(vec, iter, stdx::not_last_element);
    for (const auto& element : vec)
        std::cout << element << ' '; // 7 1 2 3 4 5 6
    std::cout << std::endl << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
