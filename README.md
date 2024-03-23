# RESTful Nested-Diff

REST API and web UI for [Nested-Diff.py](https://github.com/mr-mixas/Nested-Diff.py),
recursive diff and patch for nested structures.

**[Live Demo](https://nesteddiff.pythonanywhere.com/)**

[![PyPi](https://img.shields.io/pypi/v/nested_diff_restful.svg)](https://pypi.python.org/pypi/nested_diff_restful)
[![Tests](https://github.com/mr-mixas/Nested-Diff-RESTful/actions/workflows/tests.yml/badge.svg)](https://github.com/mr-mixas/Nested-Diff-RESTful/actions?query=branch%3Amaster)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/nested_diff_restful.svg)](https://pypi.org/project/nested_diff_restful/)
[![License](https://img.shields.io/pypi/l/nested_diff_restful.svg)](https://github.com/mr-mixas/Nested-Diff-RESTful/blob/devel/LICENSE)

## Install

```sh
pip install nested_diff_restful
```

## Run

```sh
nested_diff_restful --bind 127.0.0.1:8080 --workers=4
```

## Run tests

```sh
# prepare environment
python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -e .[test]

# run tests
pytest
```

## License

Licensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
