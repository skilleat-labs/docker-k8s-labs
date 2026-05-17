# 도전 과제 1 — Docker Guide를 쿠버네티스에 띄워보기

## 과제 설명

Docker의 공식 학습 가이드 앱을 **직접 YAML을 작성해서** 쿠버네티스 클러스터에 배포합니다.

지금까지 배운 내용만으로 충분히 해결할 수 있습니다.
YAML 작성부터 접속 확인까지 스스로 완성해보세요.

---

## 조건

| 항목 | 값 |
|---|---|
| 이미지 | `docker/getting-started:latest` |
| Deployment 이름 | `docker-guide` |
| 라벨 | `app: docker-guide` |
| 레플리카 수 | 2 |

---

## 요구사항

1. `challenge` 디렉토리를 생성하고 그 안에서 작업합니다.
2. Deployment YAML을 직접 작성해서 배포합니다.
3. 클러스터 외부(브라우저)에서 접속할 수 있도록 필요한 오브젝트를 스스로 판단하여 추가합니다.
4. 브라우저에서 Docker Guide 페이지가 열리면 완료입니다.

---

## 완료 기준

브라우저에서 Docker Guide 페이지가 열리면 성공입니다.

---

!!! warning "힌트 없이 도전하세요"
    어떤 포트를 사용하는지, 어떤 Service 타입이 필요한지 스스로 찾아보세요.
    막힌다면 `kubectl logs`, `kubectl describe`를 적극 활용합니다.
