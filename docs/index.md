# Container Service Labs

컨테이너 기반 서비스 운영을 직접 손으로 익히는 실습 중심 가이드입니다.
명령어를 따라 치면서 VM과 Docker, 그리고 Kubernetes가 어떻게 동작하는지 체감해 보세요.

---

## 실습 모듈

### Kubernetes 기반 서비스 운영 (15시간 · 2일)

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

[Kubernetes 기반 서비스 운영 시작하기](modules/module10/overview.md){ .md-button .md-button--primary }

---

!!! tip "실습 환경 안내"
    Kubernetes 기반 서비스 운영 실습은 **Docker Desktop 또는 Rancher Desktop** 환경을 기준으로 작성되었습니다.
    설정 방법은 [Kubernetes 기반 서비스 운영 — 1-1 가이드](modules/module10/1-1.md)를 참고하세요.
