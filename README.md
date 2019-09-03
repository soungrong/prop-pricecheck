# What the Flask Server and SQLAlchemy+sqlite DB is used for
1. To test the required client-side functionality. This involves loading HTML
templates, and routing requests to the serverless functions contained in
**gcloud.main**. Run **deploy_gcloud.sh** to generate gcloud's requirements and
deploy the serverless functions to gcloud.

2. Generate the necessary static files for deployment. This is handled by the
Flask extension **frozen-flask**, which loads the configured Flask routes,
simulates requests to them, and writes the responses to the **build** folder.
Run **deploy_netlify.sh** to generate the static files, and deploy them with
netlify.

3. The CSV data set is loaded into the Local sqlite DB, and further processing
is done to generate a flattened representation of the data set, ala NoSQL.

e.g. maximum/minimum and average prices of a property type are calculated
and inserted as a static value.

This NoSQL DB is then used as the production backend for the serverless function.
The purpose of these multiple deployment hoops is to reduce the processing and
storage overhead in production, which will hopefully keep any hosting costs low
and result in more responsive site interaction.

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