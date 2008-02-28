#!/bin/bash
for test in $(find tests -type f -name "*.py"); do
    python "$test"
done
