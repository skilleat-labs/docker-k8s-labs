#!/bin/bash
# ACR 로그인 필요: az acr login -n skilleatlab
REGISTRY=skilleatlab.azurecr.io
IMAGE=$REGISTRY/monolith

docker build -t $IMAGE:v1 .
docker push $IMAGE:v1

echo "✅ 완료: $IMAGE:v1"
