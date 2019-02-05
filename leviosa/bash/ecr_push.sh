#!/bin/bash

echo $ECR_REPO
echo $TASK_IMAGE_TAG
echo $VERSION

# Grab the project dir
PROJECT_ROOT_DIR=$(pwd)
# Login to ECR
$(aws ecr get-login --no-include-email)
# Build Image
docker build -t "$ECR_REPO:$VERSION" "$PROJECT_ROOT_DIR/app/"
# Tag image for ECR
docker tag ${ECR_REPO}:${VERSION} ${TASK_IMAGE_TAG}
# Push to ECR
docker push ${TASK_IMAGE_TAG}
