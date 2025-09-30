dnf install -y wget git tar

# 헬름 없으면 (있으면 주석 혹은 삭제)
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
bash get_helm.sh

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 네임스페이스 없으면
kubectl create namespace monitoring

helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring
