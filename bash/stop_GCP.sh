
PROJECT_ID="wired-glyph-475510-k4"  
REGION="europe-west1"
REPOSITORY="bentoml-repo"
IMAGE_NAME="building-energy-prediction"
SERVICE_NAME="building-energy-prediction"
gcloud run services delete ${SERVICE_NAME} --region ${REGION}
