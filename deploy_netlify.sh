#!/bin/bash

sh ./price_app/scripts/pre_deploy_netlify.sh

netlify deploy --dir=./price_app/build

deploy_to_production () {
    echo "Deploy to production? y/n"
    read userinput
    if [ "$userinput" = "y" ]; then
        echo "Deploying to production."
        netlify deploy --prod
        elif [ "$userinput" = "n" ]; then
            echo "Not deploying to production."
        else
            echo "Invalid input."
            deploy_to_production
        fi
}

# run container_cleanup function
deploy_to_production
