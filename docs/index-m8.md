# 모듈 8 — Docker 컨테이너 기초

가상머신(VM)과 컨테이너의 차이를 직접 체험하는 것부터 시작합니다.
VirtualBox에 Ubuntu를 설치하고, Docker로 Nginx · Redis를 띄워보며
이미지, 볼륨, 네트워크, Compose까지 실무에서 쓰는 패턴을 차례로 익힙니다.

**총 22시간 · 3일 과정**

---

## 단원 구성

| 단원 | 주제 |
|------|------|
| 1-1 | VM 직접 체험 — VirtualBox + Ubuntu 세팅 |
| 1-2 | Docker 기본 명령어와 컨테이너 생명주기 |
| 1-3 | 이미지 빌드 · 레지스트리 push/pull |
| 1-4 | 컨테이너 볼륨 — 데이터 영구 보존 |
| 1-5 | Dockerfile 최적화 · 멀티스테이지 빌드 |
| 1-6 | Docker 네트워크 — bridge · 커스텀 네트워크 |
| 1-7 | Docker Compose — 멀티 컨테이너 한 번에 실행 |

[커리큘럼 보기](modules/module8/curriculum.md){ .md-button }
[시작하기](modules/module8/1-1.md){ .md-button .md-button--primary }

---

!!! tip "실습 환경 안내"
    이 실습은 **VirtualBox + Ubuntu 24.04 VM** 환경을 기준으로 작성되었습니다.
    VM IP는 `192.168.56.10`으로 고정합니다. 설정 방법은 [1-1 가이드](modules/module8/1-1.md)를 참고하세요.
