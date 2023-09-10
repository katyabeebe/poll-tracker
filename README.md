# Poll tracker

This repository stores code to run an ETL pipeline for poll tracking data. 

# Project tree

 * [poll_tracker](./poll_tracker/) 
   * [data](./poll_tracker/data/)
      * [raw_polls.csv](./poll_tracker/data/raw_polls.csv)
      * [polls.csv](./poll_tracker/data/polls.csv)
      * [trends.csv](./poll_tracker/data/trends.csv)
   * [data_cleaning](./poll_tracker/data_cleaning/)
      * [data_cleaning.py](./poll_tracker/data_cleaning/data_cleaning.py)
   * [data_transform](./poll_tracker/data_transform/)
      * [data_transform.py](./poll_tracker/data_cleaning/data_transform.py)
   * [scripts](./poll_tracker/scripts/)
      * [extract.py](./poll_tracker/scripts/extract.py)
      * [transform.py](./poll_tracker/scripts/transform.py)
 * [tests](./tests/) 
   * [test_data_cleaning.py](./tests/test_data_cleaning.py)
   * [test_data_transform.py](./tests/test_data_transform.py)
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
5. Navigate to poll_tracker directory via `cd poll_tracker`
6. Run `poetry run python scripts/extract.py`
7. Run `poetry run python scripts/transform.py`

The result will provide the two datasets: `polls.csv` and `trends.csv`.

# Testing the pipeline

To test the pipeline components, run `make test`. 