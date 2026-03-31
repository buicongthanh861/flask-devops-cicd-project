#Flask App Production CI/CD & GitOps Pipeline

Dự án này thiết lập một quy trình DevOps toàn diện (End-to-End) để triển khai ứng dụng Flask. Hệ thống tự động hóa từ kiểm tra chất lượng mã nguồn, quét bảo mật đến việc triển khai liên tục (Continuous Delivery) lên Kubernetes theo mô hình GitOps chuyên nghiệp.

---

#Kiến trúc Hệ thống & Pipeline
Quy trình được chia thành hai phần tách biệt để đảm bảo tính bảo mật và ổn định:

1. CI Pipeline (GitHub Actions): Thực hiện Build, Test, Scan và đóng gói Docker Image.
2. CD Pipeline (GitOps - ArgoCD): Tự động đồng bộ hóa trạng thái giữa Git Repository và Kubernetes Cluster.

---

#Công nghệ & Công cụ sử dụng
- Ngôn ngữ: Python (Flask Framework)
- CI Tool: GitHub Actions
- GitOps Tool: ArgoCD (Đồng bộ hóa hạ tầng tự động)
- Containerization: Docker, DockerHub
- Orchestration: Kubernetes (K8s)
- Package Manager: Helm v3 (Quản lý Kubernetes Manifests)
- Quality & Security: SonarCloud, Snyk, Flake8
- Cấu hình: YAML, YQ

---

#Kubernetes Infrastructure (Helm)
Ứng dụng được đóng gói dưới dạng Helm Chart, giúp quản lý các tài nguyên K8s một cách nhất quán:

- Deployment: Quản lý vòng đời Pod, hỗ trợ chiến lược Rolling Update để Zero-Downtime.
- Service: Cung cấp ClusterIP để kết nối nội bộ giữa các thành phần.
- Ingress: Điều hướng lưu lượng từ ngoài vào Cluster (Domain/Path-based routing).
- Horizontal Pod Autoscaler (HPA): Tự động tăng/giảm số lượng Pod dựa trên mức độ sử dụng tài nguyên thực tế.
- Resource Limits: Thiết lập CPU/Memory limits để đảm bảo tính ổn định cho Cluster.

---

#Quy trình GitOps Workflow
Đây là điểm cốt lõi của dự án, giúp tự động hóa việc triển khai:

- CI Completion: Sau khi Docker Image được đẩy lên DockerHub thành công, GitHub Actions sẽ dùng tool "yq" để cập nhật tag mới vào file values.yaml của Helm Chart.
- Automated Commit: Bot tự động commit thay đổi tag vào repository cấu hình hạ tầng.
- ArgoCD Synchronization: ArgoCD phát hiện sự thay đổi trên Git và thực hiện "Sync" để kéo phiên bản mới nhất về Kubernetes Cluster.
- Drift Detection: Đảm bảo trạng thái trên Cluster luôn khớp với cấu hình trong Git (Source of Truth).

---

#Bảo mật & Chất lượng Code (Shift-Left)
- Static Analysis: SonarCloud phân tích mã nguồn để phát hiện bug và code smells sớm.
- Dependency Scan: Snyk quét các thư viện trong requirements.txt để loại bỏ các gói có lỗ hổng bảo mật.
- Linting: Flake8 đảm bảo code tuân thủ tiêu chuẩn PEP8.
- Quality Gate: Chặn toàn bộ quy trình nếu code không vượt qua các bài kiểm tra an toàn.

---

#Tính năng nổi bật
- Hoàn toàn tự động (Full Automation): Không cần can thiệp thủ công từ khi Push Code đến khi App chạy trên K8s.
- Khả năng mở rộng: Sẵn sàng chịu tải cao nhờ cấu hình HPA và Ingress.
- Khả năng phục hồi: Dễ dàng Rollback phiên bản cũ chỉ bằng cách revert commit trên Git.
- Tối ưu hiệu suất: Sử dụng Docker Layer Caching giúp giảm 60-70% thời gian build.

---
Dự án được xây dựng nhằm trình diễn kỹ năng chuyên sâu về CI/CD Pipeline, Cloud-native Infrastructure và tư duy vận hành GitOps hiện đại.