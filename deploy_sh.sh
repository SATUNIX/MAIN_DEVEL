#!/bin/bash

# Build and test code
make
make test

# Deploy code
./mainRun.sh
