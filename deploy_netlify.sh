#!/bin/bash

sh ./app-server/pre_deploy.sh

netlify deploy --dir=./app-server/app_server/build

deploy_to_production () {
    echo "Deploy to production? y/n"
    read userinput
    if [ "$userinput" = "y" ]; then
        echo "Deploying to production."
        netlify deploy --prod --dir=./app-server/app_server/build
        elif [ "$userinput" = "n" ]; then
            echo "Not deploying to production."
        else
            echo "Invalid input."
            deploy_to_production
        fi
}

# run container_cleanup function
deploy_to_production
