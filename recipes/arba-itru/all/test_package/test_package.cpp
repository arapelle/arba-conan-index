#include <arba/itru/intrusive_ref_counter.hpp>
#include <arba/itru/weak_intrusive_ptr.hpp>
#include <arba/itru/version.hpp>

#include <iostream>

class intrusive_data : public itru::intrusive_ref_counters<>
{
public:
    explicit intrusive_data(const std::string& str) : data(str) {}
    std::string data;
};

int main()
{
    std::cout << std::format("arba-itru {}", itru::version) << std::endl;

    itru::shared_intrusive_ptr data_siptr = itru::make_shared_intrusive_ptr<intrusive_data>("hello there");
    itru::shared_intrusive_ptr data_siptr_2 = data_siptr;
    itru::weak_intrusive_ptr<intrusive_data> data_wiptr(data_siptr);
    itru::weak_intrusive_ptr data_wiptr_2 = data_wiptr;
    std::cout << data_siptr->use_count() << std::endl;
    std::cout << data_siptr->latent_count() << std::endl;
    std::cout << data_wiptr.use_count() << std::endl;
    std::cout << std::boolalpha << data_wiptr.expired() << std::endl;
    itru::shared_intrusive_ptr data_siptr_3 = data_wiptr_2.lock();
    data_siptr.release();
    data_siptr_2.release();
    std::cout << data_wiptr.use_count() << std::endl;
    std::cout << std::boolalpha << data_wiptr.expired() << std::endl;
    data_siptr_3.release();
    std::cout << data_wiptr.use_count() << std::endl;
    std::cout << std::boolalpha << data_wiptr.expired() << std::endl;

    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
