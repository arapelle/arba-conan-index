#include <arba/meta/type_traits/value_or_default.hpp>
#include <arba/meta/type_traits/value_or_generate.hpp>
#include <arba/meta/version.hpp>
#include <cstdlib>
#include <iostream>

template <class ValueType, class OptionType>
std::string tfunc(const ValueType& input_value, OptionType& input_option)
{
    decltype(auto) value(meta::value_or_default(input_value, 531));
    decltype(auto) option(meta::value_or_generate(input_option, [] { return 642; }));
    std::string value_prefix = "D";
    std::string option_prefix = "D";

    if constexpr (!std::is_same_v<std::remove_cvref_t<ValueType>, meta::default_t>)
    {
        value_prefix = "V";
    }

    if constexpr (!std::is_same_v<std::remove_cvref_t<OptionType>, meta::default_t>)
    {
        option_prefix = "V";
        option += 1;
    }

    return std::format("{}{} {}{}", value_prefix, static_cast<int>(value), option_prefix, static_cast<int>(option));
}

int main()
{
    int option = 0;
    std::cout << tfunc(meta::default_v, meta::default_v) << " ; " << option << std::endl;
    std::cout << tfunc(meta::default_v, option) << " ; " << option << std::endl;
    std::cout << tfunc(42, option) << " ; " << option << std::endl;
    std::cout << "EXIT SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
