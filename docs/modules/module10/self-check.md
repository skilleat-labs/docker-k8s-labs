# 모듈 10 — 스스로 해보기

가이드 없이 혼자서 요구사항을 읽고 YAML을 작성하고, 동작을 확인하는 최종 점검입니다.
명령어 힌트는 최소화했습니다. 막히면 힌트를 펼쳐보세요.

---

## 주제 1. kubectl 클러스터 탐색

**요구사항**

1. 클러스터에 노드가 몇 개인지, 각 노드의 OS와 컨테이너 런타임을 한 번에 확인하세요.
2. Control Plane 컴포넌트(kube-apiserver, etcd, kube-scheduler 등)가 실행 중인 네임스페이스와 Pod 목록을 출력하세요.
3. `kube-apiserver` Pod를 describe하여 어떤 포트를 사용하는지 확인하세요.

**성공 조건**

```
# 노드 OS·런타임 포함 출력 예시
NAME             STATUS   ROLES           VERSION   INTERNAL-IP   OS-IMAGE         CONTAINER-RUNTIME
docker-desktop   Ready    control-plane   v1.29.x   ...           Docker Desktop   docker://...

# Control Plane Pod 목록 확인
NAME                                     READY   STATUS    NAMESPACE
kube-apiserver-docker-desktop            1/1     Running   kube-system
etcd-docker-desktop                      1/1     Running   kube-system
...
```

<details>
<summary>힌트 보기</summary>

- `-o wide` 옵션을 사용하면 OS와 런타임 정보가 추가됩니다.
- `-n kube-system` 옵션으로 네임스페이스를 지정합니다.
- `kubectl describe pod <이름> -n kube-system` 으로 상세 정보를 확인합니다.

</details>

---

## 주제 2. Pod & Deployment

### 미션 1 — Deployment 배포 및 버전 관리

**요구사항**

1. 아래 조건으로 Deployment를 YAML 파일로 작성하고 배포하세요.
   - 이름: `my-deploy`
   - 이미지: `skilleat/rollout-demo:v1.0.0`
   - replicas: 3
   - label: `app: my-deploy`
2. `port-forward`로 `http://localhost:8080`에 접속해 파란색 페이지가 뜨는지 확인하세요.
3. 이미지를 `skilleat/rollout-demo:v2.0.0`으로 롤링 업데이트하세요.
4. 업데이트 후 초록색 페이지가 뜨는지 확인하세요.
5. 직전 버전(v1.0.0)으로 롤백하세요.

**성공 조건**

```bash
# 롤백 후 이미지 확인
kubectl describe deployment my-deploy | grep Image
# Image: skilleat/rollout-demo:v1.0.0
```

<details>
<summary>힌트 보기</summary>

- `kubectl set image deployment/<이름> <컨테이너명>=<이미지>:<태그>`
- `kubectl rollout undo deployment/<이름>`
- `kubectl rollout history deployment/<이름>` 으로 히스토리 확인

</details>

---

### 미션 2 — ReplicaSet 자동 복구 확인

**요구사항**

1. `my-deploy`의 Pod 중 하나를 직접 삭제하세요.
2. Pod가 자동으로 복구되어 다시 3개가 되는지 실시간으로 확인하세요.

**성공 조건**

```bash
kubectl get pods -l app=my-deploy
# Pod 3개가 Running 상태
```

<details>
<summary>힌트 보기</summary>

- `kubectl delete pod <pod이름>`
- `kubectl get pods -l app=my-deploy -w` 로 실시간 감시

</details>

---

### 미션 3 — 스케일 조정

**요구사항**

1. `my-deploy`를 replicas 5로 늘리세요.
2. 확인 후 다시 2로 줄이세요.

**성공 조건**

```bash
kubectl get pods -l app=my-deploy
# 조정된 수만큼 Pod가 Running
```

<details>
<summary>힌트 보기</summary>

- `kubectl scale deployment <이름> --replicas=<수>`

</details>

---

## 주제 3. Service

### 미션 4 — ClusterIP + DNS 통신

**요구사항**

1. `my-deploy`를 가리키는 ClusterIP Service(`my-svc`, port 80 → targetPort 80)를 YAML로 작성하세요.
2. 임시 curl Pod를 실행해 **Service 이름(DNS)** 으로 통신이 되는지 확인하세요.
3. `kubectl get endpoints my-svc`로 Pod IP 목록을 확인하고, `kubectl get pods -o wide`의 Pod IP와 비교하세요.

**성공 조건**

```bash
kubectl run curl-test --image=curlimages/curl:latest --restart=Never -it --rm \
  -- curl http://my-svc
# HTTP 200 응답
```

<details>
<summary>힌트 보기</summary>

- Service YAML의 `spec.selector`가 Deployment의 Pod label과 일치해야 합니다.
- ClusterIP는 클러스터 내부 Pod에서만 접근 가능합니다.

</details>

---

### 미션 5 — NodePort 외부 노출

**요구사항**

1. `my-deploy`를 NodePort로 외부에 노출하는 Service(`my-nodeport`, nodePort: 30090)를 작성하세요.
2. 로컬 터미널에서 `curl http://localhost:30090`으로 응답을 받으세요.

**성공 조건**

```bash
curl http://localhost:30090
# HTML 응답
```

<details>
<summary>힌트 보기</summary>

- `spec.type: NodePort`
- `ports` 아래에 `nodePort: 30090` 추가

</details>

---

## 주제 4. ConfigMap & Secret

### 미션 6 — ConfigMap + Secret 주입

**요구사항**

1. 아래 값을 담은 ConfigMap `my-config`를 YAML로 작성하세요.
   - `APP_ENV: staging`
   - `DB_HOST: postgres-svc`
   - `DB_PORT: "5432"`

2. 아래 값을 담은 Secret `my-secret`을 작성하세요 (`stringData` 사용).
   - `DB_PASSWORD: mypassword456`

3. 아래 Pod를 작성하고 배포하세요.
   - 이름: `config-pod`
   - 이미지: `busybox:1.36`
   - command: `sh -c "echo APP=$APP_ENV DB=$DB_HOST PASS=$DB_PASSWORD && sleep 3600"`
   - ConfigMap 전체를 `envFrom`으로 주입
   - Secret에서 `DB_PASSWORD`만 `env.valueFrom`으로 주입

**성공 조건**

```bash
kubectl logs config-pod
# APP=staging DB=postgres-svc PASS=mypassword456
```

<details>
<summary>힌트 보기</summary>

- `envFrom.configMapRef.name: my-config`
- `env[].valueFrom.secretKeyRef.name: my-secret`, `key: DB_PASSWORD`

</details>

---

### 미션 7 — ConfigMap 변경 반영 차이

**요구사항**

1. `my-config`의 `APP_ENV` 값을 `production`으로 변경하세요.
2. `config-pod`에서 환경변수가 즉시 바뀌는지 확인하세요.
3. 볼륨 마운트 방식과 환경변수 방식의 갱신 차이를 한 문장으로 설명해보세요.

**성공 조건**

- 환경변수 방식: Pod 재시작 전에는 `APP_ENV=staging` 유지 확인
- 볼륨 마운트 방식: 약 1분 후 자동 갱신 확인 (이미 아는 경우 설명으로 대체 가능)

<details>
<summary>힌트 보기</summary>

- `kubectl edit configmap my-config`
- 환경변수 방식은 Pod 시작 시점에 한 번만 읽습니다.
- 볼륨 마운트 방식은 kubelet이 주기적으로 파일을 갱신합니다.

</details>

---

## 주제 5. Ingress

### 미션 8 — 경로 기반 라우팅

**요구사항**

1. 아래 두 앱을 배포하세요.

   | Deployment | 응답 메시지 | Service |
   |---|---|---|
   | `coffee-app` | `Hello from Coffee` | `coffee-svc` (port 80 → 5678) |
   | `tea-app` | `Hello from Tea` | `tea-svc` (port 80 → 5678) |

   - 이미지: `hashicorp/http-echo:latest`
   - args: `-text=<메시지>`, `-listen=:5678`

2. Nginx Ingress Controller가 설치되어 있다고 가정하고, 아래 라우팅 규칙을 가진 Ingress를 작성하세요.
   - host: `cafe.local`
   - `/coffee` → `coffee-svc`
   - `/tea` → `tea-svc`
   - annotation: `nginx.ingress.kubernetes.io/rewrite-target: /`

3. `/etc/hosts`에 `127.0.0.1 cafe.local`을 등록하세요.

**성공 조건**

```bash
curl http://cafe.local/coffee
# Hello from Coffee

curl http://cafe.local/tea
# Hello from Tea
```

<details>
<summary>힌트 보기</summary>

- `spec.ingressClassName: nginx`
- `rules[0].host: cafe.local`
- paths 아래에 `/coffee`, `/tea` 각각 지정

</details>

---

## 주제 6. PersistentVolume / PVC

### 미션 9 — 데이터 영속성 확인

**요구사항**

1. StorageClass `manual`을 사용하는 PV(`my-pv`, 1Gi, hostPath: `/tmp/my-lab-data`)를 작성하세요.
2. `my-pv`를 사용하는 PVC(`my-pvc`, 500Mi)를 작성하세요.
3. `my-pvc`를 `/data`에 마운트하는 Pod를 배포하고, `/data/message.txt`에 `"K8s storage test"` 문자열을 저장하세요.
4. Pod를 삭제하고 새 Pod를 만들어 같은 PVC를 마운트한 뒤, `/data/message.txt` 파일이 그대로 남아있는지 확인하세요.

**성공 조건**

```bash
kubectl logs <새 pod 이름>
# K8s storage test
```

<details>
<summary>힌트 보기</summary>

- PV와 PVC의 `storageClassName`이 동일해야 바인딩됩니다.
- `volumes[].persistentVolumeClaim.claimName: my-pvc`

</details>

---

## 주제 7. Probe

### 미션 10 — Readiness Probe로 트래픽 차단

**요구사항**

1. 아래 조건으로 Deployment를 작성하세요.
   - 이름: `probe-app`, 이미지: `nginx:1.25`, replicas: 2
   - Readiness Probe: HTTP GET `/`, port 80, `initialDelaySeconds: 5`, `periodSeconds: 5`
   - 연결하는 Service: `probe-svc` (ClusterIP, port 80)

2. 배포 후 `kubectl get endpoints probe-svc`로 Pod 2개가 Endpoints에 등록되는지 확인하세요.

3. Pod 하나에 접속해 Nginx를 중지하세요.
   ```bash
   kubectl exec <pod이름> -- nginx -s stop
   ```

4. 해당 Pod가 Endpoints에서 제거되는지 확인하세요.

**성공 조건**

```bash
kubectl get pods -l app=probe-app
# 한 Pod: READY 0/1, 다른 Pod: READY 1/1

kubectl get endpoints probe-svc
# Endpoint가 1개로 줄어있음
```

<details>
<summary>힌트 보기</summary>

- `readinessProbe.httpGet.path: /`, `readinessProbe.httpGet.port: 80`
- Pod가 `Running`이더라도 READY=0/1이면 Service Endpoint에서 제외됩니다.

</details>

---

### 미션 11 — Liveness Probe 자동 재시작

**요구사항**

1. 아래 Pod를 작성하세요.
   - 이름: `liveness-test`
   - 이미지: `busybox:1.36`
   - command: `sh -c "touch /tmp/alive && sleep 20 && rm /tmp/alive && sleep 3600"`
   - Liveness Probe: `cat /tmp/alive`, `initialDelaySeconds: 5`, `periodSeconds: 5`, `failureThreshold: 3`

2. 배포 후 `kubectl get pod liveness-test -w`로 감시하면서 30~60초 후 `RESTARTS`가 증가하는지 확인하세요.

**성공 조건**

```bash
kubectl get pod liveness-test
# RESTARTS가 1 이상
```

<details>
<summary>힌트 보기</summary>

- 20초 후 `/tmp/alive` 파일이 삭제되면 Probe가 실패합니다.
- `failureThreshold: 3` × `periodSeconds: 5` = 15초 후 재시작됩니다.

</details>

---

## 주제 8. Resource requests/limits & QoS

### 미션 12 — QoS 클래스 판별

**요구사항**

아래 3개 Pod를 배포하고 각각의 QoS 클래스를 확인하세요.

| Pod 이름 | requests | limits | 예상 QoS |
|---|---|---|---|
| `pod-a` | 없음 | 없음 | ? |
| `pod-b` | cpu: 100m, memory: 128Mi | cpu: 300m, memory: 256Mi | ? |
| `pod-c` | cpu: 200m, memory: 256Mi | cpu: 200m, memory: 256Mi | ? |

이미지는 모두 `nginx:1.25`

**성공 조건**

```bash
kubectl get pod pod-a -o yaml | grep qosClass
# qosClass: BestEffort

kubectl get pod pod-b -o yaml | grep qosClass
# qosClass: Burstable

kubectl get pod pod-c -o yaml | grep qosClass
# qosClass: Guaranteed
```

<details>
<summary>힌트 보기</summary>

- requests, limits 모두 없으면 → **BestEffort**
- requests < limits (또는 일부만 설정) → **Burstable**
- requests == limits (CPU, Memory 모두) → **Guaranteed**

</details>

---

## 주제 9. HPA

### 미션 13 — HPA 자동 확장 설정

**요구사항**

1. 아래 조건으로 Deployment를 배포하세요.
   - 이름: `my-hpa-app`, 이미지: `k8s.gcr.io/hpa-example`, replicas: 1
   - `resources.requests.cpu: 100m`, `limits.cpu: 500m`
   - Service: `my-hpa-svc` (ClusterIP, port 80)

2. CPU 사용률 50% 기준으로 min 1, max 8 HPA를 YAML로 작성하여 배포하세요.

3. 부하 Pod를 실행하여 자동 확장을 확인하세요.
   ```bash
   kubectl run load \
     --image=busybox:1.36 \
     --restart=Never \
     -- sh -c "while true; do wget -q -O- http://my-hpa-svc; done"
   ```

4. REPLICAS가 늘어나는 것을 확인하고, 부하 Pod를 삭제한 뒤 다시 1로 축소되는지 확인하세요.

**성공 조건**

```bash
kubectl get hpa my-hpa-app
# REPLICAS가 부하 시 증가, 부하 제거 후 1로 복귀
```

<details>
<summary>힌트 보기</summary>

- HPA YAML에서 `scaleTargetRef.name`이 Deployment 이름과 일치해야 합니다.
- `averageUtilization: 50`
- Metrics Server가 설치되어 있어야 합니다 (`kubectl top nodes` 동작 확인).

</details>

---

## 종합 미션 — 미니 서비스 단독 배포

> 지금까지 배운 내용을 모두 활용해 하나의 서비스를 처음부터 끝까지 혼자서 만들어봅니다.

**요구사항**

아래 조건을 만족하는 K8s 리소스를 모두 작성하고 배포하세요.

1. **Namespace**: `final-lab`
2. **ConfigMap** (`final-config`): `APP_NAME=FinalApp`, `APP_PORT="8080"`
3. **Secret** (`final-secret`): `APP_SECRET_KEY=supersecret` (`stringData` 사용)
4. **Deployment** (`final-app`):
   - 이미지: `hashicorp/http-echo:latest`
   - args: `-text=Hello Final App`, `-listen=:5678`
   - replicas: 2
   - ConfigMap 전체를 `envFrom`으로 주입
   - Secret에서 `APP_SECRET_KEY`를 `env.valueFrom`으로 주입
   - Readiness Probe: TCP port 5678, `periodSeconds: 5`
   - `resources.requests.cpu: 50m`, `requests.memory: 64Mi`
5. **Service** (`final-svc`): NodePort, port 80 → targetPort 5678, nodePort: 30099
6. **HPA** (`final-hpa`): CPU 60% 기준, min 2, max 6

**성공 조건**

```bash
# 접속 확인
curl http://localhost:30099
# Hello Final App

# HPA 확인
kubectl get hpa final-hpa -n final-lab
# NAME         REFERENCE              TARGETS   MINPODS   MAXPODS   REPLICAS
# final-hpa    Deployment/final-app   ...       2         6         2

# 환경변수 확인
kubectl exec -n final-lab deployment/final-app -- env | grep -E "APP_NAME|APP_SECRET"
# APP_NAME=FinalApp
# APP_SECRET_KEY=supersecret
```

**완료 후 정리**

```bash
kubectl delete namespace final-lab
```

---

## 정답 체크리스트

| 주제 | 미션 | 완료 |
|---|---|---|
| kubectl 탐색 | 노드·Control Plane 확인 | ☐ |
| Deployment | 배포·업데이트·롤백 | ☐ |
| Deployment | ReplicaSet 자동 복구 | ☐ |
| Deployment | 스케일 조정 | ☐ |
| Service | ClusterIP + DNS | ☐ |
| Service | NodePort | ☐ |
| ConfigMap/Secret | 환경변수 주입 | ☐ |
| ConfigMap/Secret | 변경 반영 차이 이해 | ☐ |
| Ingress | 경로 기반 라우팅 | ☐ |
| PVC | 데이터 영속성 확인 | ☐ |
| Probe | Readiness 트래픽 차단 | ☐ |
| Probe | Liveness 자동 재시작 | ☐ |
| QoS | 클래스 판별 | ☐ |
| HPA | 자동 확장·축소 | ☐ |
| 종합 | 단독 배포 | ☐ |
