#!/bin/sh

set -e

DEFAULT_REPOSITORY=pypi

if [ $# -gt 0 ] ; then
    repository=$1
else
    repository=$DEFAULT_REPOSITORY
fi

version=$(grep version= setup.py | cut -d\" -f2)

python3 -m build

twine upload --repository $repository dist/*$version*

if [ $repository = $DEFAULT_REPOSITORY ] ; then
    git tag v$version
    git push
    git push --tags
fi
