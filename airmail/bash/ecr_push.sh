#!/bin/bash

set -e

printf "\n"
echo "Building to repo: $ECR_REPO"
echo "Building version: $VERSION"
printf "\n"

PROJECT_ROOT_DIR=$(pwd)
SHA=$(git rev-parse --short HEAD)
$(aws ecr get-login --no-include-email)
docker build -t "$ECR_REPO" "$PROJECT_ROOT_DIR/$APP_DIR/"
docker tag ${ECR_REPO} ${TASK_IMAGE_TAG}
docker push ${TASK_IMAGE_TAG}

# Tag ECR image with version and SHA of latest commit
IMG_MANIFEST=$(aws ecr batch-get-image --repository-name $ECR_REPO --image-ids imageTag=latest --query 'images[].imageManifest' --output text)

aws ecr put-image --repository-name $ECR_REPO --image-tag $VERSION --image-manifest "$IMG_MANIFEST" > /dev/null
aws ecr put-image --repository-name $ECR_REPO --image-tag $SHA --image-manifest "$IMG_MANIFEST" > /dev/null
