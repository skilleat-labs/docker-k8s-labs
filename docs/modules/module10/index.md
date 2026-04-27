# 모듈 10 — Kubernetes 기반 서비스 운영 및 확장 설계

모듈 10은 로컬 Kubernetes 환경(Docker Desktop / Rancher Desktop)에서 K8s 핵심 리소스를 직접 배포하고, Probe·HPA·Ingress 등 운영 기능을 실습합니다.

## 실습 환경

| 환경 | 비고 |
|---|---|
| Docker Desktop (Mac/Windows) | Kubernetes 탭에서 Enable Kubernetes 활성화 |
| Rancher Desktop | containerd 또는 dockerd 선택 가능 |
| AKS (선택) | 로컬 실습에 익숙해진 후 Azure 클라우드에서 동일 실습 반복 |

## 단원별 가이드

### 단원 1. K8s 기초와 철학

- [1-1. 실습 환경 설정 (Docker Desktop / Rancher Desktop)](./1-1.md)
- [1-2. kubectl 기본 명령어 & 클러스터 구조 탐색](./1-2.md)

### 단원 2. 핵심 리소스와 설정 관리

- [2-1. Pod & Deployment 실습](./2-1.md)
- [2-2. Service 실습 (ClusterIP · NodePort · port-forward)](./2-2.md)
- [2-3. ConfigMap & Secret 실습](./2-3.md)
- [2-4. 미니 블로그 3-tier 배포 실습](./2-4.md)

### 단원 3. 네트워킹과 스토리지

- [3-1. Ingress 실습 (Nginx Ingress Controller)](./3-1.md)
- [3-2. PersistentVolume / PVC 실습](./3-2.md)

### 단원 4. 안정성과 확장 관리

- [4-1. Probe 설정 실습 (Liveness · Readiness · Startup)](./4-1.md)
- [4-2. Resource requests/limits & QoS 실습](./4-2.md)
- [4-3. HPA (Horizontal Pod Autoscaler) 실습](./4-3.md)
