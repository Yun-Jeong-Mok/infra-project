# Openstack 환경 기반 프라이빗 클라우드 인프라 구축

### 인프라 (총 16대 인스턴스로 구성)
Openstack, Kubernetes, Helm, Podman, Buildah, Flannel, HAProxy, Zerotier, Tekton, Ansible, wrk, Prometheus, Alertmanager, Grafana, Loki, Promtail, Metrics-server,  Minio, Velero, Rook-ceph, Docker-registry, Gitea

### 웹 서비스
Javascript, TailwindCSS, Astro, Python, Scikit-learn, InsightFace, FastAPI, ChromaDB

### 외부 서비스
Slack(웹훅 알람), HostingKR(노드포트로 도메인 호스팅), Github, Quay.io

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
