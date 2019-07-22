#!/bin/bash

sh ./price_app/scripts/pre_deploy_gcloud.sh

# https://cloud.google.com/functions/docs/deploying/filesystem
gcloud functions deploy arbitrary_name_of_function \
    --source=./price_app/gcloud \
    --env-vars-file=.env.yaml \
    --runtime python37 \
    --entry-point=name_of_parent_function_in_main_py \
    --memory=128MB \
    --timeout=30s \
    --trigger-http
