# Container Service Labs

컨테이너 기반 서비스 운영을 직접 손으로 익히는 실습 중심 가이드입니다.
명령어를 따라 치면서 VM과 Docker, 그리고 Kubernetes가 어떻게 동작하는지 체감해 보세요.

---

## 실습 모듈

### 모듈 8 — Docker 컨테이너 기초 (22시간 · 3일)

가상머신(VM)과 컨테이너의 차이를 직접 체험하는 것부터 시작합니다.
VirtualBox에 Ubuntu를 설치하고, Docker로 Nginx · Redis를 띄워보며
이미지, 볼륨, 네트워크, Compose까지 실무에서 쓰는 패턴을 차례로 익힙니다.

| 단원 | 주제 |
|------|------|
| 1-1 | VM 직접 체험 — VirtualBox + Ubuntu 세팅 |
| 1-2 | Docker 기본 명령어와 컨테이너 생명주기 |
| 1-3 | 이미지 빌드 · 레지스트리 push/pull |
| 1-4 | 컨테이너 볼륨 — 데이터 영구 보존 |
| 1-5 | Dockerfile 최적화 · 멀티스테이지 빌드 |
| 1-6 | Docker 네트워크 — bridge · 커스텀 네트워크 |
| 1-7 | Docker Compose — 멀티 컨테이너 한 번에 실행 |

[모듈 8 시작하기](modules/module8/overview.md){ .md-button .md-button--primary }

---

### 모듈 10 — Kubernetes 핵심 운영 (15시간 · 2일)

Docker로 익힌 컨테이너를 클러스터 위에서 운영하는 방법을 배웁니다.
Pod · Deployment · Service부터 Ingress, PVC, HPA까지
실제 운영 환경에서 마주치는 시나리오를 실습합니다.

| 단원 | 주제 |
|------|------|
| 1-1 | 실습 환경 설정 (Docker Desktop / Rancher Desktop) |
| 1-2 | kubectl 기본 명령어 · 클러스터 구조 탐색 |
| 2-1 | Pod & Deployment 실습 |
| 2-2 | Service — ClusterIP · NodePort · port-forward |
| 2-3 | ConfigMap & Secret |
| 2-4 | 미니 블로그 3-tier 배포 실습 |
| 3-1 | Ingress & Gateway API |
| 3-2 | PersistentVolume / PVC |
| 4-1~4-3 | Probe · 리소스 관리 · HPA |

[모듈 10 시작하기](modules/module10/overview.md){ .md-button }

---

!!! tip "실습 환경 안내"
    모듈 8 실습은 **VirtualBox + Ubuntu 24.04 VM** 환경을 기준으로 작성되었습니다.
    VM IP는 `192.168.56.10`으로 고정합니다. 설정 방법은 [모듈 8 — 1-1 가이드](modules/module8/1-1.md)를 참고하세요.
