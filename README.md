# Arba Conan Index #

Arba Conan Index is the source index of recipes of the `arba` packages for Conan.

# Install

- Clone this repository.
```shell
git clone https://github.com/arapelle/arba-conan-index.git
```

- Add this *local recipes index* as a Conan remote.
```shell
conan remote add arba-conan-index ./arba-conan-index
```

# Use

- You can list all available recipes:

```shell
conan list "*" -r arba-conan-index
```

- You can create a package:

example:
```shell
conan create ./arba-conan-index/recipes/arba-vrsn/all --version=0.4.1 --build="missing"
```

# License

[MIT License](./LICENSE.md) © arba-conan-index
