#!/bin/bash

SRC=tema
TESTS=tests
OUT=out
PYTHON_CMD=python3.8

# Cleanup the previous run's temporary files
rm -f ${TESTS}/*.out.sorted

# Run tests
   rm -f "${TESTS}/08".out
   echo "Starting test $i"
   ${PYTHON_CMD} test.py "${TESTS}/08.in" > "${TESTS}/08.out"
   echo "Finished test $i"
   ${PYTHON_CMD} check_test.py 8 "${TESTS}/08.out" "${TESTS}/08.ref.out"
   diff "${TESTS}/08.ref.out" "${TESTS}/08.out.sorted"
# Pylint checks - the pylintrc file being in the same directory
# Uncoment the following line to check your implementation's code style :)
# ${PYTHON_CMD} -m pylint ${SRC}/*.py