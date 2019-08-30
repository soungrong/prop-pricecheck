#!/bin/bash

sh ./gc-form/pre_deploy.sh

# https://cloud.google.com/functions/docs/deploying/filesystem
gcloud functions deploy pricecheck-gc-form \
    --source=./gc-form/gc_form \
    --runtime python37 \
    --entry-point=process_form \
    --memory=128MB \
    --timeout=30s \
    --trigger-http
