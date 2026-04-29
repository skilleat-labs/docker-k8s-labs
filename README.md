# Container Service Labs

컨테이너 기반 서비스 운영 실습 가이드

**가이드 사이트**: https://skilleat-labs.github.io/docker-k8s-labs/

---

## 구성

```
.
├── docs/                   # 실습 가이드 문서 (MkDocs)
│   └── modules/
│       ├── module8/        # Docker 실습 (1-1 ~ 1-7)
│       └── module10/       # Kubernetes 실습
├── docker-images/          # 실습용 이미지 소스코드
│   └── env-lab/            # 환경변수 실습 이미지
└── mkdocs.yml              # MkDocs 설정
```

## 실습 이미지

실습에 사용하는 이미지는 `docker-images/` 폴더에서 관리합니다.

| 이미지 | 태그 | 설명 |
|--------|------|------|
| `skilleatlab.azurecr.io/frontend` | `v4-kb5` | 미니 블로그 frontend (Nginx) |
| `skilleatlab.azurecr.io/backend` | `v4-kb5` | 미니 블로그 backend (Flask) |
| `skilleatlab.azurecr.io/env-lab` | `hardcoded` | 환경변수 실습 - 하드코딩 문제 시연 |
| `skilleatlab.azurecr.io/env-lab` | `v1` | 환경변수 실습 - ENV 기반 개선 버전 |
| `skilleatlab.azurecr.io/env-lab` | `arg-demo` | 환경변수 실습 - ARG vs ENV 시연 |
| `skilleatlab.azurecr.io/monolith` | `v1` | 모놀리식 아키텍처 실습 - 카페 주문 앱 (Flask + SQLite 내장) |

### 이미지 빌드 및 푸시

```bash
az acr login -n skilleatlab
cd docker-images/env-lab
./build-and-push.sh
```

## 로컬 문서 서버 실행

```bash
pip install mkdocs-material
mkdocs serve
```

`http://localhost:8000` 에서 확인할 수 있습니다.
