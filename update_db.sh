#!/bin/bash

create_migration () {
    echo "Create migration? y/n"
    read userinput
    if [ "$userinput" = "y" ]; then
        echo "Creating migration."
        pipenv run flask db migrate
        elif [ "$userinput" = "n" ]; then
            echo "Skipping migration creation."
        else
            echo "Invalid input."
            create_migration
        fi
}

apply_migrations () {
    echo "Apply migrations? y/n"
    read userinput
    if [ "$userinput" = "y" ]; then
        echo "Applying migrations."
        pipenv run flask db upgrade
        elif [ "$userinput" = "n" ]; then
            echo "Skipping apply migrations."
        else
            echo "Invalid input."
            apply_migrations
        fi
}

create_migration
apply_migrations
