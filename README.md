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