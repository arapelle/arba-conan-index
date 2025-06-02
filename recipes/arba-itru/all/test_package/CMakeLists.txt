cmake_minimum_required(VERSION 3.15)

project(PackageTest CXX)

set(lib_namespace "arba")
set(lib_base_name "itru")
find_package(${lib_namespace}-${lib_base_name} CONFIG REQUIRED)

if(arba-itru_VERSION VERSION_GREATER_EQUAL "0.5.0")
    set(sources test_package.cpp)
else()
    set(sources test_package__0_3_to_0_4.cpp)
endif()

set(test_program "test_package")
add_executable(${test_program} ${sources})

if(TARGET ${lib_namespace}::${lib_base_name})
    set(lib_target "${lib_namespace}::${lib_base_name}")
else()
    set(lib_target "${lib_namespace}::${lib_base_name}-static")
endif()
target_link_libraries(${test_program}
    PRIVATE
        ${lib_target}
)

target_compile_features(${test_program} PRIVATE cxx_std_20)
