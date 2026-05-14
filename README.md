# Flask App – CI/CD & GitOps Pipeline

Deploy ứng dụng Flask lên Kubernetes theo mô hình GitOps, tự động hoàn toàn từ push code đến chạy trên cluster.

---

## Stack

| Layer | Tool |
|-------|------|
| App | Python / Flask |
| CI | GitHub Actions |
| CD | ArgoCD |
| Container | Docker / DockerHub |
| Orchestration | Kubernetes + Helm v3 |
| Quality & Security | Flake8, SonarCloud, Snyk |

---

## Pipeline

```
push → main
    │
    ├── [1] Test & Scan
    │       ├── Flake8 (lint)
    │       ├── SonarCloud (static analysis)
    │       └── Snyk (dependency scan)
    │
    ├── [2] Build & Push Docker Image
    │       └── <dockerhub>:<github.sha>
    │
    └── [3] GitOps Update
            ├── Dùng yq cập nhật image tag trong values.yaml
            ├── Auto-commit vào repo infra
            └── ArgoCD sync → K8s cluster
```

---

## Kubernetes (Helm)

- **Deployment** — Rolling Update, zero downtime
- **Service** — ClusterIP
- **Ingress** — Domain/path-based routing
- **HPA** — Auto-scale theo CPU/Memory
- **Resource Limits** — CPU & Memory limits cho từng pod

---

## GitOps Flow

1. CI push image xong → yq ghi tag mới vào `values.yaml`
2. Bot commit lên repo infra
3. ArgoCD phát hiện diff → tự động sync lên cluster
4. Cluster luôn khớp với Git (single source of truth)

Rollback = revert commit trên Git.

---

## Secrets cần cấu hình

| Secret | Dùng cho |
|--------|----------|
| `DOCKER_USERNAME` / `DOCKER_PASSWORD` | Push Docker Hub |
| `SONAR_TOKEN` | SonarCloud |
| `SNYK_TOKEN` | Snyk scan |
| `INFRA_DEPLOY_TOKEN` | Push sang repo infra |
