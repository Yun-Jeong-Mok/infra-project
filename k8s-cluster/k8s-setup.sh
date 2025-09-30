#!/bin/bash

KUBERNETES_VERSION=v1.32
CRIO_VERSION=v1.32

swapoff -a
sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1

echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/01-ip_forward.conf
echo "br_netfilter" > /etc/modules-load.d/01-br_netfilter.conf
modprobe br_netfilter
sysctl -p > /dev/null

setenforce 0
systemctl disable --now firewalld > /dev/null 2>&1

echo ""

cat <<EOF | tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/$KUBERNETES_VERSION/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/$KUBERNETES_VERSION/rpm/repodata/repomd.xml.key
EOF

echo ""

cat <<EOF | tee /etc/yum.repos.d/cri-o.repo
[cri-o]
name=CRI-O
baseurl=https://download.opensuse.org/repositories/isv:/cri-o:/stable:/$CRIO_VERSION/rpm/
enabled=1
gpgcheck=1
gpgkey=https://download.opensuse.org/repositories/isv:/cri-o:/stable:/$CRIO_VERSION/rpm/repodata/repomd.xml.key
EOF

dnf install -y container-selinux cri-o kubelet kubeadm kubectl  

systemctl enable --now crio > /dev/null 2>&1
systemctl enable --now kubelet > /dev/null 2>&1

echo -e "--------------  check configuration  --------------\n"
sysctl net.ipv4.ip_forward
lsmod | grep br_netfilter
getenforce
systemctl status firewalld | grep -E "inactive|disabled"
systemctl status crio | grep -E "active|enabled"
systemctl status kubelet | grep -E "active|enabled"
echo -e "\n---------------------------------------------------\n\n\n"

echo "------------------------------------------"
echo -e "\n   ### k8s installation completed  ###   \n"
echo "------------------------------------------"
