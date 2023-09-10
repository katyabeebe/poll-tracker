# Poll tracker

This repository stores code to run an ETL pipeline for poll tracking data. 

# Project tree

 * [src](./src) 
   * [file21.ext](./dir2/file21.py)
   * [file22.ext](./dir2/file22.py)
   * [file23.ext](./dir2/file23.py)
 * [deploy](./deploy)
   * [file11.ext](./dir1/file11.py)
   * [file12.ext](./dir1/file12.py)
 * [LICENSE](./LICENSE)
 * [makefile](./makefile)
 * [poetry.lock](./poetry.lock)
 * [pyproject.toml](./pyproject.toml)
 * [README.md](./README.md)

# Getting started
If you have the M1 chip, run softwareupdate --install-rosetta to install Rosetta2 locally.

1. Use `pyenv` to run python version mentioned in `.python-version`
2. Install [poetry](https://poetry.eustace.io/docs/#installation) if necessary
3. Run `make dev` to create virtual env
4. Run `poetry shell` to activate virtual env