#!/usr/bin/env python
import sys
import argparse
import os
import subprocess
import time
from pathlib import Path

import yaml

SCRIPT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
RECIPES_DIR = SCRIPT_DIR / "../recipes"


class TestSuite:
    def test_packages(self):
        self.init_settings()
        versions_str = "all versions" if self.test_all_versions else "latest version"
        print(f"""Treating {versions_str} of the following packages: {self.package_names}""")
        start_time = time.monotonic()
        tests_result = 0
        for package_name in self.package_names:
            if not test_suite.test_package(package_name, self.test_all_versions, self.test_tests):
                tests_result = 1
                break
        duration = time.monotonic() - start_time
        print(f"total duration: {duration:.03f} seconds")
        return tests_result

    def init_settings(self):
        args = self.__parse_args()
        if len(args.packages) > 0:
            self.package_names = args.packages
        else:
            with open(SCRIPT_DIR / "all.txt") as all_recipes_file:
                self.package_names = all_recipes_file.read().split()
        self.test_all_versions = args.all_versions
        self.test_tests = args.test
        self.built_library_types = []
        if not args.shared and not args.static:
            self.built_library_types = ["shared", "static"]
        else:
            if args.shared:
                self.built_library_types.append("shared")
            if args.static:
                self.built_library_types.append("static")
        self.build_types = []
        if not args.release and not args.debug:
            self.build_types = ["Release", "Debug"]
        else:
            if args.release:
                self.build_types.append("Release")
            if args.debug:
                self.build_types.append("Debug")

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog='arba-conan-index recipe tester',
                                         description='Test creating packages from recipes with different settings.')
        parser.add_argument("-V", "--all-versions", help="all versions of a package", action="store_true")
        parser.add_argument("-t", "--test", help="build and run unit tests", action="store_true")
        parser.add_argument("-s", "--shared", help="test shared libraries", action="store_true")
        parser.add_argument("-a", "--static", help="test static libraries", action="store_true")
        parser.add_argument("-d", "--debug", help="test debug", action="store_true")
        parser.add_argument("-r", "--release", help="test release", action="store_true")
        parser.add_argument("packages", nargs="*")
        return parser.parse_args()

    def test_package(self, package_name: str, all_versions: bool = False, test: bool = True):
        print(f"# Testing package {package_name}")
        project_path = RECIPES_DIR / package_name
        with open(project_path / "config.yml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        versions = config["versions"]
        if all_versions:
            for version, data in versions.items():
                if not self.test_specific_package(project_path, version, data, test):
                    return False
            return True
        else:
            latest_item = list(versions.items())[-1]
            latest_version = latest_item[0]
            data = latest_item[1]
            return self.test_specific_package(project_path, latest_version, data, test)

    def test_specific_package(self, project_path: Path, version, data, test: bool = True):
        package_name = project_path.name
        print(f"## Testing specific package {package_name}/{version}")
        recipe_path = project_path / data["folder"]
        with open(f"{recipe_path}/conanfile.py", 'r') as conanfile:
            conanfile_content = conanfile.read()
        is_header_library = conanfile_content.find("package_type = \"header-library\"") != -1
        if is_header_library:
            library_types = ["header-only"]
        else:
            library_types = self.built_library_types
        for build_type in self.build_types:
            print(f"### Build type: {build_type}")
            for library_type in library_types:
                print(f"#### Library Type: {library_type}")
                library_type_option = ""
                if library_type != "header-only":
                    library_type_is_shared = library_type == "shared"
                    library_type_option = f"""-o "&:shared={library_type_is_shared}\""""
                cmd = f"""conan create {recipe_path} --build=missing \\
                --version {version} -s "&:build_type={build_type}" {library_type_option} -c:a "&:tools.build:skip_test={not test}\""""
                print(f"  .cmd: {cmd}")
                cmd = cmd.replace("\\", "")
                cmd = cmd.replace('"', "")
                start_time = time.monotonic()
                p_res = subprocess.run(cmd.split(), capture_output=True, timeout=180, encoding="utf-8")
                cmd_duration = time.monotonic() - start_time
                print(f"  .duration: {cmd_duration:.03f} seconds")
                if p_res.returncode == 0:
                    print(f"  .result: {package_name}/{version} {build_type} OK")
                else:
                    print(f"  .result: {package_name}/{version} {build_type} ERR ({p_res.returncode})")
                    print(f"  .output:{{{{{str(p_res.stdout)}}}}}")
                    print(f"  .error:{{{{{str(p_res.stderr)}}}}}")
                    return False
        return True


if __name__ == '__main__':
    test_suite = TestSuite()
    result = test_suite.test_packages()
    print("EXIT SUCCESS" if result == 0 else "EXIT FAILURE")
    sys.exit(result)
