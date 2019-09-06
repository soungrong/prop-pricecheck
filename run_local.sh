#!/bin/bash

cd app-server
npm run build
poetry run flask run
