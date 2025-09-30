# ☁️ Openstack 환경 기반 프라이빗 클라우드 인프라 구축

## ⚙️🛠️ 기술 스택

### 💻 인프라 (총 16대 인스턴스 구성)
![OpenStack](https://img.shields.io/badge/OpenStack-EA2046?logo=openstack&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?logo=helm&logoColor=white)
![Podman](https://img.shields.io/badge/Podman-892CA0?logo=podman&logoColor=white)
![Buildah](https://img.shields.io/badge/Buildah-EE0000?logo=redhat&logoColor=white)
![Flannel](https://img.shields.io/badge/Flannel-00ADEF?logo=flannel&logoColor=white)
![HAProxy](https://img.shields.io/badge/HAProxy-1064A0?logo=haproxy&logoColor=white)
![Zerotier](https://img.shields.io/badge/Zerotier-FFAA00?logo=zerotier&logoColor=black)
![Tekton](https://img.shields.io/badge/Tekton-FD495C?logo=tekton&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)
![wrk](https://img.shields.io/badge/wrk-555555?logo=gnu&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Alertmanager](https://img.shields.io/badge/Alertmanager-FFCC00?logo=prometheus&logoColor=black)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)
![Loki](https://img.shields.io/badge/Loki-FFCC00?logo=grafana&logoColor=black)
![Promtail](https://img.shields.io/badge/Promtail-1C1C1C?logo=grafana&logoColor=white)
![Metrics-server](https://img.shields.io/badge/Metrics--server-326CE5?logo=kubernetes&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?logo=minio&logoColor=white)
![Velero](https://img.shields.io/badge/Velero-4B7BEC?logo=kubernetes&logoColor=white)
![Rook-Ceph](https://img.shields.io/badge/Rook--Ceph-2D2D2D?logo=ceph&logoColor=white)
![Docker Registry](https://img.shields.io/badge/Docker--Registry-2496ED?logo=docker&logoColor=white)
![Gitea](https://img.shields.io/badge/Gitea-609926?logo=gitea&logoColor=white)

---

## 🌐 웹 서비스
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?logo=tailwind-css&logoColor=white)
![Astro](https://img.shields.io/badge/Astro-BC52EE?logo=astro&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![InsightFace](https://img.shields.io/badge/InsightFace-FF6F61?logo=ai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-20232A?logo=database&logoColor=white)

---

## 🔗 외부 서비스
![Slack](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)
![HostingKR](https://img.shields.io/badge/HostingKR-0D47A1?logo=google-cloud&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Quay.io](https://img.shields.io/badge/Quay.io-EE0000?logo=redhat&logoColor=white)


---

## k8s 클러스터 관리 인스턴스 및 k8s 클러스터

### helm version
k8s 패키지 관리 도구
(loki-stack, prometheus-grafana, velero, rook-ceph, tekton, flannel 등 설치)

version.BuildInfo{Version:"v3.18.6", GitCommit:"b76a950f6835474e0906b96c9ec68a2eff3a6430", GitTreeState:"clean", GoVersion:"go1.24.6"}

### tekton-cli version
k8s CI/CD 자동화 툴 (gitea webhook 연동으로 트리거 설정)
git clone -> buildah build -> buildah push -> kubectl set image ...(롤링 업데이트)

Client version: 0.42.0
Pipeline version: v1.4.0
Triggers version: v0.33.0
Dashboard version: v0.61.0

### kubectl version 
k8s 클러스터 관리 인스턴스 및 k8s 클러스터
(총 9대 : 컨트롤 3, 워커 5, 로드밸런서 1)

Client Version: v1.32.9
Kustomize Version: v5.5.0
Server Version: v1.32.9

### velero version 
백업 스케줄링 (miniO 연동 Openstack 내 1대, 외부 1대)

Client:
        Version: v1.17.0
        Git commit: 3172d9f99c3d501aad9ddfac8176d783f7692dce
Server:
        Version: v1.17.0

### buildah version
이미지 빌드 (quay.io에서 pull, 내부 저장소에 push)

Version:         1.39.4
Go Version:      go1.23.9 (Red Hat 1.23.9-1.el9_6)
Image Spec:      1.1.0
Runtime Spec:    1.2.0
CNI Spec:        1.1.0
libcni Version:  
image Version:   5.34.3
Git Commit:      
Built:           Tue Jun 17 17:55:27 2025
OS/Arch:         linux/amd64
BuildPlatform:   linux/amd64

---
## 내부 저장소용 인스턴스 (1대)

- gitea - 내부 깃 저장소
- docker registry - 내부 이미지 저장소
- registry-ui - 이미지 저장소 web UI
- miniO - 백업용 객체 저장소

### podman container images

docker.io/gitea/gitea       latest    
docker.io/minio/minio       latest     
docker.io/quiq/registry-ui  latest      
docker.io/library/registry  latest
registry.k8s.io/pause       3.10

### podman version

Client:       Podman Engine
Version:      5.4.0
API Version:  5.4.0
Go Version:   go1.23.9 (Red Hat 1.23.9-1.el9_6)
Built:        Wed Jul  9 00:04:52 2025
OS/Arch:      linux/amd64

---

## 앤서블 부하테스트 클러스터 (컨트롤 1대, 커맨드 5대)
HTTP GET Flooding 시뮬레이션

### ansible version
부하테스트 클러스터 구성 및 공격 자동화

ansible [core 2.14.18]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.9/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.9.21 (main, Feb 10 2025, 00:00:00) [GCC 11.5.0 20240719 (Red Hat 11.5.0-5)] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True

### wrk version
오픈소스 경량 부하테스트 도구

wrk 4.2.0 [epoll] Copyright (C) 2012 Will Glozer

---

## 외부 백업 저장소 (개인 노트북 사용)
Hyper-V 환경에서 Ubuntu 24.04 server ISO 이미지 사용
내부 저장소와 동일한 버전의 Podman과 minio 컨테이너 이미지 사용
