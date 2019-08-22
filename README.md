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

# Create/Apply migrations
sh update_db.sh

# Import dataset from CSV file
sh populate_db.sh

# Run interactive shell
pipenv run shell

# Run Flask server for local dev
sh run_local.sh

# Deploy gcloud serverless function
sh deploy_gcloud.sh

# Deploy static files in build folder to netlify
sh deploy_netlify.sh