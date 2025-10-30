#!/bin/bash
set -e

PROJECT_ID="wired-glyph-475510-k4"  
REGION="europe-west1"
REPOSITORY="bentoml-repo"
IMAGE_NAME="building-energy-prediction"
SERVICE_NAME="building-energy-prediction"

echo "Tagging and pushing Docker image..."
docker tag building_energy_prediction:latest \
    ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:latest

docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:latest

echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:latest \
    --region ${REGION} \
    --platform managed \
    --port 3000 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10

echo "Deployment complete!"
gcloud run services describe ${SERVICE_NAME} \
    --region ${REGION} \
    --format 'value(status.url)'
