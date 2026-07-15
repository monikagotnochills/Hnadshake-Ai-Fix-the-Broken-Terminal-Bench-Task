#!/bin/bash
set -e

if pytest /tests/test_outputs.py -rA; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi