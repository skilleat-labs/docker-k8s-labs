#!/bin/bash
# ACR 로그인 필요: az acr login -n skilleatlab
REGISTRY=skilleatlab.azurecr.io

docker build -t $REGISTRY/msa-cafe-frontend:v1 ./frontend
docker push $REGISTRY/msa-cafe-frontend:v1

docker build -t $REGISTRY/msa-cafe-backend:v1 ./backend
docker push $REGISTRY/msa-cafe-backend:v1

echo "✅ 완료"
echo "  $REGISTRY/msa-cafe-frontend:v1"
echo "  $REGISTRY/msa-cafe-backend:v1"
