#!/bin/bash

# cd into directory where this script exists, if executed outside of this dir
cd "${0%/*}"

poetry run generate-static
