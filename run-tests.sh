#!/bin/bash

PYTHON="${PYTHON:-python3.12}"
OAREPO_VERSION="${OAREPO_VERSION:-12}"
TESTS_VENV=.venv-tests

if test -d $TESTS_VENV ; then
	rm -rf $TESTS_VENV
fi

$PYTHON -m venv $TESTS_VENV
. $TESTS_VENV/bin/activate

pip install -U setuptools pip wheel
pip install "oarepo[tests]==${OAREPO_VERSION}.*"
pip install -e .

(
    find oarepo_glitchtip -name '*.py' | grep -v '-' | tr '/' '.' | sed 's/\.__init__\.py//' | sed 's/\.py$//' | sed 's/^/import /'
) > $TESTS_VENV/all_imports.py
python $TESTS_VENV/all_imports.py