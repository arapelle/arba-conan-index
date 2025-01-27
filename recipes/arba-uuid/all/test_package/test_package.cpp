#include <arba/uuid/uuid.hpp>
#include <arba/uuid/version.hpp>

#include <cstdlib>
#include <iostream>

int main()
{
    std::cout << std::format("arba-uuid-{}", arba::uuid::version) << std::endl;
    arba::uuid::uuid id("03b0d57c-a6bd-40de-bbb7-d26534801bb0");
    std::cout << "uuid: " << id << std::endl;
    uuid::uuid id2("78fdfce9-76f0-4088-ba95-713cf711781a");
    std::cout << "uuid: " << id2 << std::endl;
    std::cout << "uuid hash: " << std::hash<uuid::uuid>{}(id2) << std::endl;
    std::cout << "uuid: " << uuid::uuid::make_random_uuid() << std::endl;
    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
