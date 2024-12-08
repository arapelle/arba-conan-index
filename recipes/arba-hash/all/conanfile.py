import os, re

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import load, copy, rmdir, apply_conandata_patches, export_conandata_patches, get

class ArbaHashRecipe(ConanFile):
    project_namespace = "arba"
    project_base_name = "hash"
    name = f"{project_namespace}-{project_base_name}"
    package_type = "header-library"
    description = "A C++ library providing version classes."
    url = "https://github.com/arapelle/arba-hash"
    homepage = "https://github.com/arapelle/arba-hash"
    topics = ("hash", "murmur")
    license = "MIT"
    author = "Aymeric Pellé"

    win_bash = os.environ.get('MSYSTEM', None) is not None
    no_copy_source = True

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False],
        "test": [True, False]
    }
    default_options = {
        "shared": True, 
        "fPIC": True,
        "test": False
    }

    implements = ["auto_shared_fpic"]

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder,
            strip_root=True)
        apply_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, 20)

    def requirements(self):
        self.requires("arba-vrsn/[^0.4]", transitive_headers=True, transitive_libs=True)

    def build_requirements(self):
        self.test_requires("gtest/[^1.14]")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        upper_name = f"{self.project_namespace}_{self.project_base_name}".upper()
        tc.variables[f"{upper_name}_LIBRARY_TYPE"] = "SHARED" if self.options.shared else "STATIC"
        if self.options.test:
            tc.variables[f"BUILD_{upper_name}_TESTS"] = "TRUE"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if self.options.test:
            cmake.ctest(cli_args=["--progress", "--output-on-failure"])

    def package(self):
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        postfix = "" if self.options.shared else "-static"
        name = self.name + postfix
        self.cpp_info.libs = [name]
        self.cpp_info.set_property("cmake_target_name", name.replace('-', '::', 1))
