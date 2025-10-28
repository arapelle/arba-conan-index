import os, re

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy, rmdir, apply_conandata_patches, export_conandata_patches, get
from conan.tools.scm import Version

required_conan_version = ">=2.2.0"

class ArbaCppxRecipe(ConanFile):
    project_namespace = "arba"
    project_base_name = "cppx"
    name = f"{project_namespace}-{project_base_name}"
    package_type = "header-library"

    # Optional metadata
    description = "A C++ library providing essential features."
    url = "https://github.com/arapelle/arba-cppx"
    homepage = "https://github.com/arapelle/arba-cppx"
    topics = ("C++", "version", "semver", "semantic-version", "preprocessor", "no-exceptions")
    license = "MIT"
    author = "Aymeric Pellé"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "execution_backend": ["", "TBB"],
        "use_system_execution_backend": [True, False]
    }
    default_options = {
        "execution_backend": "",
        "use_system_execution_backend": False
    }

    # Build
    win_bash = os.environ.get('MSYSTEM', None) is not None
    no_copy_source = True

    # Other
    implements = ["auto_header_only"]

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder,
            strip_root=True)
        apply_conandata_patches(self)

    def configure(self):
        if not self.options.use_system_execution_backend:
            if self.options.execution_backend == "TBB" and self.settings.build_type == "Debug":
                self.options["onetbb/*"].tbbmalloc = False

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, 20)

    def requirements(self):
        if not self.options.use_system_execution_backend:
            if self.options.execution_backend == "TBB":
                self.requires("onetbb/[^2022.0]", transitive_libs=True)

    def build_requirements(self):
        self.test_requires("gtest/[^1.14]")

    def generate(self):
        upper_name = f"{self.project_namespace}_{self.project_base_name}".upper()
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables[f"{upper_name}_EXECUTION_BACKEND"] = self.options.execution_backend
        build_test = False
        if self.version >= Version("0.4.0"):
            build_test = not self.conf.get("tools.build:skip_test", default=True)
        if build_test:
            tc.variables[f"BUILD_{upper_name}_TESTS"] = "TRUE"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        build_test = False
        if self.version >= Version("0.4.0"):
            build_test = not self.conf.get("tools.build:skip_test", default=True)
        if build_test:
            cmake.build()
            cmake.ctest(cli_args=["--progress", "--output-on-failure"])

    def package(self):
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.set_property("cmake_target_name", self.name.replace('-', '::'))
        if self.options.execution_backend != "":
            self.cpp_info.defines = ["ARBA_CPPX_EXECUTION_ALL_STD_POLICIES=true"]
