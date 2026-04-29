#!/bin/bash
# ACR 로그인 필요: az acr login -n skilleatlab
REGISTRY=skilleatlab.azurecr.io
IMAGE=$REGISTRY/env-lab

# 1. 하드코딩 버전
docker build -f Dockerfile.hardcoded -t $IMAGE:hardcoded .
docker push $IMAGE:hardcoded

# 2. ENV 기반 정상 버전
docker build -f Dockerfile -t $IMAGE:v1 .
docker push $IMAGE:v1

# 3. ARG vs ENV 시연 버전
docker build -f Dockerfile.arg-demo \
  --build-arg BUILD_VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date +%Y-%m-%d) \
  -t $IMAGE:arg-demo .
docker push $IMAGE:arg-demo

echo "✅ 완료"
echo "  $IMAGE:hardcoded"
echo "  $IMAGE:v1"
echo "  $IMAGE:arg-demo"
