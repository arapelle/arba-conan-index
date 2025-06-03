import os, re

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy, rmdir, apply_conandata_patches, export_conandata_patches, get
from conan.tools.scm import Version

required_conan_version = ">=2.2.0"

class ArbaApptRecipe(ConanFile):
    project_namespace = "arba"
    project_base_name = "appt"
    name = f"{project_namespace}-{project_base_name}"
    package_type = "library"

    # Optional metadata
    description = "A C++ library providing application classes embedding useful tools."
    url = "https://github.com/arapelle/arba-appt"
    homepage = "https://github.com/arapelle/arba-appt"
    topics = ("application", "app")
    license = "MIT"
    author = "Aymeric Pellé"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False],
        "test": [True, False],
        "use_spdlog": [True, False]
    }
    default_options = {
        "shared": True, 
        "fPIC": True,
        "test": False,
        "use_spdlog": True
    }

    # Build
    win_bash = os.environ.get('MSYSTEM', None) is not None
    no_copy_source = True

    # Other
    implements = ["auto_shared_fpic"]

    def config_options(self):
        if self.settings.get_safe("os") == "Windows":
            self.options.rm_safe("fPIC")
        if self.version < Version("0.17.0"):
            del self.options.use_spdlog

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder,
            strip_root=True)
        apply_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, 20)

    def requirements(self):
        if self.version >= Version("0.16.0"):
            self.requires("arba-core/[^0.30]", transitive_headers=True, transitive_libs=True)
            self.requires("arba-stdx/[^0.3]", transitive_headers=True, transitive_libs=True)
            self.requires("arba-rsce/[^0.5]", transitive_headers=True, transitive_libs=True)
            self.requires("arba-evnt/[^0.7]", transitive_headers=True, transitive_libs=True)
        else:
            self.requires("arba-core/[^0.29]", transitive_headers=True, transitive_libs=True)
            self.requires("arba-stdx/[^0.2]", transitive_headers=True, transitive_libs=True)
            self.requires("arba-rsce/[^0.4]", transitive_headers=True, transitive_libs=True)
            self.requires("arba-evnt/[^0.6]", transitive_headers=True, transitive_libs=True)
        if self.version < Version("0.17.0") or self.options.use_spdlog:
            self.requires("spdlog/[^1.8]", transitive_headers=True, transitive_libs=True)

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
        if self.version >= Version("0.17.0"):
            tc.variables[f"{upper_name}_USE_SPDLOG"] = "TRUE" if self.options.use_spdlog else "FALSE"
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
        self.cpp_info.set_property("cmake_target_name", name.replace('-', '::', 1))
        if self.settings.build_type == "Debug":
            name += "-d"
        self.cpp_info.libs = [name]
