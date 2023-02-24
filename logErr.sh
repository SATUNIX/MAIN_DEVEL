#!/bin/bash

# Run tests with debugging enabled
python -m pdb mytests.py

# Analyze log files
grep "ERROR" /var/log/myapp.log | less
