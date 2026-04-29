# 모듈 8 · 실기 과제형 평가지

## 엔터프라이즈 CA 도입과 컨테이너 기반 설계

---

## ■ 기본 정보

| 항목 | 내용 |
|------|------|
| 과정명 | 컨테이너 기반 Composable Architecture 설계 |
| 모듈 | 모듈 8 — 엔터프라이즈 CA 도입과 컨테이너 기반 설계 |
| 평가 유형 | 실기 과제형 (개인) |
| 배점 | 100점 (항목별 부분 점수제) |
| 평가 시간 | 120분 |
| 허용 도구 | 강의 자료, 공식 문서 (인터넷 허용) |

---

## ■ 시나리오

온라인 쇼핑몰 **'ShopCore'** 는 10년 이상 운영된 Python 기반 모놀리식 애플리케이션입니다. 최근 블랙프라이데이 기간 급격한 트래픽 증가로 결제 기능 과부하 시 전체 서비스가 중단되는 장애가 반복되고 있습니다. CTO는 이를 해결하기 위해 CA(Composable Architecture) 전환 프로젝트를 승인하였습니다.

**실습 환경 서비스 구성 (스켈레톤 코드 제공)**

- **Order Service** — 주문/결제 처리 (포트 8001, `GET /health`, `GET /orders`)
- **Product Service** — 상품/재고 관리 (포트 8002, `GET /health`, `GET /products`)
- **Notification Service** — 알림 발송 (포트 8003, `GET /health`, `POST /notify`)

---

## ■ 제공 파일 (스켈레톤 코드)

!!! info "shopcore-skeleton.zip"
    📦 `shopcore-skeleton.zip`을 압축 해제한 후 과제를 수행하세요.
    앱 소스코드(`main.py`, `requirements.txt`)는 **수정하지 않습니다.**

```
shopcore-skeleton/
├── order/
│   ├── app/main.py          ← FastAPI 앱 (수정 금지)
│   ├── requirements.txt     ← 의존성 목록 (수정 금지)
│   └── Dockerfile           ← ✏️ 직접 작성
├── product/
│   ├── app/main.py
│   ├── requirements.txt
│   └── Dockerfile           ← ✏️ 직접 작성
├── notification/
│   ├── app/main.py
│   ├── requirements.txt
│   └── Dockerfile           ← ✏️ 직접 작성
├── docker-compose.yml       ← ✏️ 직접 작성
└── .env.example             ← 참고용 (직접 .env 생성)
```

---

## ■ 제출물 안내

**제출 디렉터리 구조**

```
[이름]_과제/
├── report/CA전략보고서.pdf
├── order/Dockerfile
├── product/Dockerfile
├── notification/Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

| No. | 파일명 | 내용 | 형식 |
|-----|--------|------|------|
| ① | CA전략보고서.pdf (또는 .docx) | CA 전환 설계 분석 보고서 (A4 1~2페이지) | PDF / Word |
| ② | order / product / notification Dockerfile | Dockerfile (서비스별 각각 작성) | 텍스트 |
| ③ | docker-compose.yml | 다중 서비스 환경 및 네트워크 설계 | YAML |
| ④ | [이름]_과제.zip | 위 ①~③ 및 .env.example, README.md 포함 | ZIP |

---

## ■ 요구사항 1 — CA 전환 설계 (최대 35점)

CA전략보고서(A4 기준 1~2페이지)를 작성하여 아래 항목을 포함하시오.
제공된 템플릿 형식을 활용해도 됩니다.

### 1-1. 모놀리식 구조의 한계 분석

- ShopCore의 현재 구조에서 발생하는 기술적 확장 한계를 구체적으로 서술하시오.
- 배포 단위, 장애 전파, 특정 기능 스케일아웃 불가 문제를 포함할 것
- 블랙프라이데이 장애 상황을 참고하여 구체적인 예시를 포함할 것 (짧게 서술 가능)

### 1-2. 서비스 분리 설계

- 3개 서비스(Order, Product, Notification)의 분리 이유와 경계를 서술하시오.
- 팀 ↔ 서비스 매핑 표 또는 다이어그램을 포함할 것 (텍스트 표로도 충분)

### 1-3. MSA 전환 타당성 판단

- **기술적 관점**: 독립 배포, 장애 격리, 독립 확장
- **비즈니스 관점**: 운영 비용, 개발 속도, 조직 변화 관리
- 기술적·비즈니스적 관점 중 하나 이상을 근거로 최종 도입 권고 여부를 명시할 것

### 채점 기준

| 채점 항목 | 세부 기준 | 점수 |
|-----------|-----------|------|
| 모놀리식 한계 분석 | 배포·장애·스케일아웃 문제 중 2가지 이상 구체적으로 서술 | 12점 |
| 서비스 분리 근거 | 3개 서비스(Order/Product/Notification) 분리 이유와 경계 서술 | 10점 |
| MSA 도입 권고 | 도입 권고 여부를 이유 1가지 이상 근거로 명시 | 5점 |
| 팀↔서비스 매핑 | 팀 구조와 서비스 매핑 표 또는 다이어그램 포함 | 4점 |
| Conway's Law 적용 【심화】 | Conway's Law 정의를 인용하고 ShopCore에 적용한 근거를 논리적으로 서술 | 4점 |
| **합계** | | **35점** |

---

## ■ 요구사항 2 — 컨테이너 패키징 (최대 45점)

제공된 스켈레톤 코드(Python FastAPI)를 기반으로 서비스별 Dockerfile을 작성하시오.
3개 서비스(order, product, notification) 모두 동일한 조건을 적용하되, Dockerfile은 각각 작성한다.

### 2-1. 멀티 스테이지 빌드 구성

- 【기본】 단일 스테이지 빌드: `python:3.11-slim` 베이스로 의존성 설치 및 앱 실행
- 【심화·추가 점수】 멀티 스테이지 빌드: `builder → runtime` 2단계로 이미지 경량화
- 이미지 크기 200MB 이하 달성 시 추가 점수 부여
- `python:3.11-slim` 또는 `python:3.11-alpine` 권장

### 2-2. 보안 및 재현 가능성

- Non-root 유저를 생성하여 애플리케이션을 실행할 것
- 베이스 이미지 버전을 `latest`가 아닌 명시적 태그로 고정할 것
- `ARG` 또는 `ENV`를 활용하여 포트, 서비스명 등을 외부 주입 가능하도록 설계할 것
- `requirements.txt`를 먼저 복사하여 의존성 레이어를 캐시할 것

!!! warning "채점 핵심"
    채점 시 `docker build` 명령으로 빌드를 수행합니다. **빌드 성공 여부가 핵심 채점 기준입니다.**
    빌드 후 컨테이너 실행하여 `http://localhost:{포트}/health` 응답 확인까지 검증합니다.

### 채점 기준

| 채점 항목 | 세부 기준 | 점수 |
|-----------|-----------|------|
| Dockerfile 작성 | 3개 서비스 Dockerfile 파일 모두 제출 (서비스당 2점) | 6점 |
| 빌드 성공 | `docker build` 명령으로 각 이미지 빌드 성공 (서비스당 4점) | 12점 |
| /health 응답 | 컨테이너 실행 후 `/health` 엔드포인트 정상 응답 (서비스당 3점) | 9점 |
| 멀티 스테이지 빌드 【심화】 | builder → runtime 2단계 멀티 스테이지 구성 (서비스당 3점) | 9점 |
| Non-root 유저 설정 【심화】 | 앱 실행 유저를 non-root로 생성 및 적용 (서비스당 2점) | 6점 |
| 이미지 크기 200MB 이하 【심화】 | 최종 이미지 크기 200MB 이하 달성 | 3점 |
| **합계** | | **45점** |

---

## ■ 요구사항 3 — 네트워크 구성 (최대 20점)

`docker-compose.yml`을 작성하여 ShopCore 3개 서비스를 하나의 환경에서 구성하시오.

### 3-1. 서비스 구성 및 이름 기반 통신

- 3개 서비스(order, product, notification) 모두 컨테이너로 구성
- 서비스는 컨테이너 이름으로 상호 통신할 것 (IP 하드코딩 금지)
- 각 서비스의 Dockerfile을 `build` 지시어로 참조할 것
- `healthcheck` 및 `depends_on` 설정 권장 (미설정 시 감점 없음)

### 3-2. 네트워크 격리 설계

- 외부에 노출되는 서비스와 내부 서비스 간 네트워크를 분리하여 설계할 것
- `frontend` 네트워크: 외부 포트 바인딩 허용
- 【심화·추가 점수】 `backend` 네트워크: `internal: true` 적용으로 인터넷 차단
- 각 서비스가 속하는 네트워크를 명시적으로 선언할 것

### 3-3. 환경 변수 분리

- 서비스명, 버전 등 설정 값은 `.env` 파일로 분리할 것
- `.env.example` 파일을 함께 제출할 것 (실제 값 없이 키만 기입)

!!! warning "채점 핵심"
    채점 시 `docker compose up --build` 명령으로 전체 환경 기동 후 3개 서비스의 `/health` 엔드포인트를 확인합니다.

### 채점 기준

| 채점 항목 | 세부 기준 | 점수 |
|-----------|-----------|------|
| 3서비스 기동 성공 | `docker compose up --build` 후 3개 서비스 모두 정상 기동 | 8점 |
| 이름 기반 통신 | 컨테이너 이름으로 상호 통신 설정 (IP 하드코딩 금지) | 4점 |
| .env 파일 분리 | `.env` + `.env.example` 파일 제출, 설정 값 외부화 | 4점 |
| 네트워크 격리 【심화】 | frontend/backend 네트워크 분리, backend에 `internal: true` 적용 | 4점 |
| **합계** | | **20점** |

---

## ■ 권장 시간 배분

| 시간 | 활동 | 산출물 |
|------|------|--------|
| 0 ~ 20분 | CA 전략 보고서 작성 (1~2페이지, 핵심 항목 중심) | CA전략보고서.pdf |
| 20 ~ 70분 | Dockerfile 작성 (3개 서비스) 및 빌드 검증 | order/product/notification Dockerfile |
| 70 ~ 105분 | docker-compose.yml 작성 및 전체 기동 확인 | docker-compose.yml |
| 105 ~ 120분 | README 작성, 압축 및 최종 제출 | [이름]_과제.zip |

---

## ■ 유의사항

!!! danger "필독"
    - 앱 소스코드(`main.py`, `requirements.txt`)는 수정하지 않습니다.
    - Dockerfile 및 `docker-compose.yml`은 강사의 환경(amd64 기준)에서 실행 가능해야 합니다.
    - 보고서는 본인의 언어로 작성하며, 타인의 결과물 복사 시 0점 처리합니다.
    - 제출 기한 이후에는 접수하지 않으며, 미제출 항목은 0점 처리합니다.
    - 질문은 평가 시작 전 10분 내에만 허용하며, 평가 중 질의응답은 불가합니다.

---

*— 수고하셨습니다 —*
