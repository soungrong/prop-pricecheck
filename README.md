# Run Flask server for local dev
sh run_local.sh

# Deploy gcloud serverless function
sh deploy_gcloud.sh

# Deploy static files in build folder to netlify
sh deploy_netlify.sh