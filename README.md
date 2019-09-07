**Warning! This project is pretty much pre-alpha. Peruse at your own risk.**


# Project Overview
The goal of this project is to help people make more informed property purchasing
decisons, by processing publicly-available **property listing** data in a meaningful
way, and returning the results in a form that doesn't require a user to do
mental kungfu.

Results are currently restricted to listings within Kuala Lumpur only.

## Current Behavior
1. _Required_ user inputs are location (with Google Maps Autocomplete),
and number of rooms/plus rooms/bathrooms/car parks.
2. The form is POSTed to a gcloud function, which runs a query routine involving
a MongoDB instance.
3. A record that's closest to the desired location and criteria is returned.

## Current Architecture
**gc-form package**: The layout and naming conventions within this package conform to the deployment
requirements of a gcloud function. Running `deploy_gcloud.sh` deploys `gc_form/`
as a gcloud function, with the necessary configuration and files self-contained.

**app-server package**: This contains a bare minimum Flask app, which simulates the gcloud function
endpoint, and holds the source of static files that's later built and deployed
with Netlify.


# Dataset Labels
To increase the probability of returning a listing match, all query arguments
except for **town** and **property_type** are turned into representative integers.
The integer picked is a relative score based on assumed desirability.
This allows for query arguments to use a _less than or equals to_ condition when
returning matches.

> e.g. if the query is for a **Fully Furnished** listing but there's no exact match,
> the next closest match would be a listing that's **Partly Furnished**.

> e.g. if the query is for an **Intermediate** listing, the next most desireable
> match is for a **Corner** listing, given that **EndLot** is usually the least
> desireable out of the 3 possibilities.

1. Furnishing
- Fully Furnished = 1
- Partly Furnished = 0.5
- Unfurnished = 0 (if unspecified, assume it is unfurnished)

Listings that have an unspecified level of furnishing is set as **Unfurnished**,
based on the assumption that **Furnishing** is an obvious selling point that
would have been specified, if there was any furnishing at all.

2. Position
- Intermediate = 1
- Corner = 0.75
- EndLot = 0.5
- Not specified = 0


# Scalingo MongoDB (mongo-sandbox plan)
For some reason, an admin user and db is created along with the instance,
but the password isn't provided. Additional users can't be created either.
So we create an instance with the CLI tool, and then reset the password.

## Download CLI tool
https://doc.scalingo.com/cli

## Set a region
https://doc.scalingo.com/platform/internals/regions
```
$ scalingo config --region <region_code_name>
```

## Create instance
```
$ scalingo -a <app_name> addons-add mongodb mongo-sandbox
```

## Instance setup
Find out what the default user and db is called first.
```
$ scalingo -a <app_name> mongo-console
$ show users
```

Then use these values to change the user password.
```
$ use <db_name>
$ db.changeUserPassword("<username>", "<password>")
```


# App Scripts/CLI Commands
Run these while you're _in_ the app-server/ DIR.

**Import dataset from CSV file**
```
poetry run flask csv-to-pandas
```

**Run interactive shell**
```
poetry run shell
```

___
These exist in the project root, but can be called from wherever.

**Run Flask server for local dev**
```
sh run_local.sh
```

**Deploy gc-form/gc_form/ as gcloud serverless function**
```
sh deploy_gcloud.sh
```

**Deploy app-server/app_server/ static files to Netlify**
```
sh deploy_netlify.sh
```