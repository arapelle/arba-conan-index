#include <arba/itru/intrusive_ref_counter.hpp>
#include <arba/itru/intrusive_weak_ptr.hpp>
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

    itru::intrusive_shared_ptr data_isptr = itru::make_intrusive_shared_ptr<intrusive_data>("hello there");
    itru::intrusive_shared_ptr data_isptr_2 = data_isptr;
    itru::intrusive_weak_ptr<intrusive_data> data_iwptr(data_isptr);
    itru::intrusive_weak_ptr data_iwptr_2 = data_iwptr;
    std::cout << data_isptr->use_count() << std::endl;
    std::cout << data_isptr->latent_count() << std::endl;
    std::cout << data_iwptr.use_count() << std::endl;
    std::cout << std::boolalpha << data_iwptr.expired() << std::endl;
    itru::intrusive_shared_ptr data_isptr_3 = data_iwptr_2.lock();
    data_isptr.release();
    data_isptr_2.release();
    std::cout << data_iwptr.use_count() << std::endl;
    std::cout << std::boolalpha << data_iwptr.expired() << std::endl;
    data_isptr_3.release();
    std::cout << data_iwptr.use_count() << std::endl;
    std::cout << std::boolalpha << data_iwptr.expired() << std::endl;

    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
