#!/bin/bash

helm repo add grafana https://grafana.github.io/helm-charts
helm repo add loki https://grafana.github.io/helm-charts
helm repo update

# 프로메테우스 + 그라파나, 로키 + 프롬테일 구성
helm install loki grafana/loki-stack -n logging --set promtail.enabled=true prometheus.enabled=true, grafana.enabled=true, loki.enabled=true

# 로키스택 그라파나 비번
kubectl get secret --namespace monitoring loki-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
