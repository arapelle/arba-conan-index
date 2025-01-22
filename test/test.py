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


def test_package(package_name: str, all_versions: bool = False, test: bool = True):
    print(f"# Testing package {package_name}")
    project_path = RECIPES_DIR / package_name
    with open(project_path / "config.yml", 'r') as config_file:
        config = yaml.safe_load(config_file)
    versions = config["versions"]
    if all_versions:
        for version, data in versions.items():
            if not test_specific_package(project_path, version, data, test):
                return False
        return True
    else:
        latest_item = list(versions.items())[-1]
        latest_version = latest_item[0]
        data = latest_item[1]
        return test_specific_package(project_path, latest_version, data, test)


def test_specific_package(recipe_path: Path, version, data, test: bool = True):
    package_name = recipe_path.name
    print(f"## Testing specific package {package_name}/{version}")
    folder = data["folder"]
    for build_type in ("Release", "Debug"):
        cmd = f"""conan create {recipe_path / folder}  --build=missing 
            --version {version}
            -s "&:build_type={build_type}" 
            -o "&:test={test}" """
        print(f"### Build type: {build_type}\n  .cmd: {cmd}")
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
    parser = argparse.ArgumentParser(prog='arba-conan-index recipe tester',
                                     description='Test creating packages from recipes with different settings.')
    parser.add_argument("-a", "--all", help="all versions of a package", action="store_true")
    parser.add_argument("-t", "--test", help="compile and run unit tests", action="store_true")
    parser.add_argument("packages", nargs="*")
    args = parser.parse_args()
    package_names = args.packages if len(args.packages) > 0 else [x for x in os.listdir(RECIPES_DIR)]
    print(f"""Treating {"all versions" if args.all else "latest version"} of the following packages: {package_names}""")
    for package_name in package_names:
        if not test_package(package_name, args.all, args.test):
            print("EXIT FAILURE")
            sys.exit(1)
    print("EXIT SUCCESS")
