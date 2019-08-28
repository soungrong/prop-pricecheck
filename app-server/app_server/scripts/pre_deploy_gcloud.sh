#!/bin/bash

# generate a requirements.txt from Pipfile
pipenv lock -r > requirements.txt
