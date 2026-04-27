# 모듈 10 개요 — Kubernetes 기반 서비스 운영

## 학습 목표

이 모듈에서는 **로컬 Kubernetes 환경**에서 K8s 핵심 리소스를 직접 배포하고,
Probe·HPA·Ingress 등 운영 기능을 실습하며 컨테이너 오케스트레이션을 체득합니다.

## 왜 Kubernetes인가?

### Docker Compose의 한계

| 상황 | Docker Compose | Kubernetes |
|------|---------------|-----------|
| 컨테이너 비정상 종료 | 수동 재시작 | 자동 재시작 (자가 치유) |
| 트래픽 급증 | 수동 스케일 | HPA 자동 스케일 |
| 무중단 배포 | 다운타임 발생 | Rolling Update |
| 멀티 노드 분산 | 불가 | 기본 지원 |
| 설정값 관리 | .env 파일 직접 관리 | ConfigMap / Secret |

### K8s가 실무에서 쓰이는 이유

> Docker는 컨테이너 하나를 잘 다루는 도구,
> Kubernetes는 수십~수천 개의 컨테이너를 자동으로 관리하는 플랫폼입니다.

## 실습 환경

| 환경 | 설치 방법 | 비고 |
|------|---------|------|
| Docker Desktop (Mac/Windows) | Kubernetes 탭 → Enable Kubernetes | 가장 간편 |
| Rancher Desktop | containerd 또는 dockerd 선택 | 오픈소스 |
| AKS (선택) | Azure Portal | 로컬 실습 후 클라우드 반복 |

## 단원 구성

| 단원 | 주제 | 핵심 리소스 |
|------|------|-----------|
| **단원 1** | K8s 기초와 철학 | kubectl, Node, Namespace |
| 1-1 | 실습 환경 설정 | Docker Desktop / Rancher Desktop |
| 1-2 | kubectl & 클러스터 탐색 | get, describe, logs, exec |
| **단원 2** | 핵심 리소스와 설정 관리 | Pod, Deployment, Service, ConfigMap |
| 2-1 | Pod & Deployment | ReplicaSet, Rolling Update |
| 2-2 | Service | ClusterIP, NodePort, port-forward |
| 2-3 | ConfigMap & Secret | 환경변수 주입, 볼륨 마운트 |
| 2-4 | 3-tier 앱 배포 | 미니 블로그 (web + api + db) |
| **단원 3** | 네트워킹과 스토리지 | Ingress, PV, PVC |
| 3-1 | Ingress | Nginx Ingress Controller, 호스트 기반 라우팅 |
| 3-2 | PersistentVolume | PV, PVC, StorageClass |
| **단원 4** | 안정성과 확장 관리 | Probe, Resource, HPA |
| 4-1 | Probe 설정 | Liveness, Readiness, Startup |
| 4-2 | Resource 관리 | requests/limits, QoS 클래스 |
| 4-3 | HPA | CPU 기반 자동 수평 확장 |

## 선수 지식

- Docker 기초 (이미지 빌드, 컨테이너 실행) — 모듈 8 수료 권장
- YAML 문법 기초
- Linux 기본 명령어
