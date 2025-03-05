#include <arba/seri/binary/io.hpp>
#include <arba/seri/polymorphism.hpp>

#include <iostream>
#include <memory>
#include <vector>

class Abstract
{
public:
    virtual ~Abstract() {}
    virtual void print() const = 0;
    virtual std::ostream& write_binary(std::ostream& stream) const = 0;
    virtual std::istream& read_binary(std::istream& stream) = 0;
};

class Cube : public Abstract
{
public:
    Cube(unsigned size = 0) : size(size) {}
    virtual ~Cube() = default;
    virtual void print() const override { std::cout << "Cube_" << size << std::endl; }

    virtual std::ostream& write_binary(std::ostream& stream) const override { return seri::write_binary(stream, size); }

    virtual std::istream& read_binary(std::istream& stream) override { return seri::read_binary(stream, size); }

    unsigned size;
};

ARBA_SERI_DEFINE_SERIALIZABLE_TYPE_ID(Cube, "45c03a9c-b94b-4168-bb23-dcf52562b9eb");
ARBA_SERI_REGISTER_INHERITANCE_RELATION(Abstract, Cube);

int main()
{
    std::vector<std::unique_ptr<Abstract>> things;
    things.push_back(std::make_unique<Cube>(2));
    things.push_back(std::make_unique<Cube>(45));
    std::vector<std::unique_ptr<Abstract>> other_things;

    std::cout << "things:" << std::endl;
    for (const auto& thing_ptr : things)
        thing_ptr->print();
    std::cout << ".\n" << std::endl;

    std::stringstream stream(std::ios::binary | std::ios::in | std::ios::out);
    seri::write_binary(stream, things);
    seri::read_binary(stream, other_things);

    std::cout << "other_things:" << std::endl;
    for (const auto& thing_ptr : other_things)
        thing_ptr->print();
    std::cout << ".\n" << std::endl;

    std::cout << "EXIT_SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
