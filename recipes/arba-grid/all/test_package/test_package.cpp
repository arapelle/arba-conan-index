#include <arba/grid/grid.hpp>
#include <arba/grid/version.hpp>

#include <iostream>
#include <string>

int main()
{
    arba::grid::grid<std::string> gr(3, 2, "----");
    gr.get(1, 1) = "Cool";

    for (uint16_t j = 0; j < gr.height(); ++j)
    {
        for (uint16_t i = 0; i < gr.width(); ++i)
            std::cout << gr.get(i, j) << "  ";
        std::cout << std::endl;
    }
    std::cout << std::endl;

    grid::grid_position::number height = gr.height();
    for (grid::grid_position pos; pos.y() < height; gr.advance(pos))
        std::cout << "[" << pos << "]: " << gr.get(pos) << std::endl;
    std::cout << std::endl;

    for (const std::string& str : gr)
        std::cout << "[" << gr.value_position(str) << "]: " << str << std::endl;
    std::cout << std::endl;

    std::cout << "TEST PACKAGE SUCCESS" << std::endl;
    return EXIT_SUCCESS;
}
