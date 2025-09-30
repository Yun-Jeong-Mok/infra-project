import requests
import time
from datetime import datetime, timedelta

PROMETHEUS_URL = "http://compute1:32200/api/v1/query"
LOKI_URL = "http://compute5:32100/loki/api/v1/query_range"

SLACK_WEBHOOK_URL = "https://hooks.slack.com/triggers/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"

def query_prometheus(query):
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": query})
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["data"]["result"]
        else:
            return []
    except Exception as e:
        print(f"[{datetime.now()}] Prometheus query error: {e}")
        return []

def query_loki(query, minutes=5):
    start_ts = int((datetime.utcnow() - timedelta(minutes=minutes)).timestamp() * 1e9)
    try:
        response = requests.get(LOKI_URL, params={"query": query, "start": start_ts})
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["data"]["result"]
        else:
            return []
    except Exception as e:
        print(f"[{datetime.now()}] Loki query error: {e}")
        return []

def main():
    while True:
        print(f"[{datetime.now()}] === Data Collection ===")

        # Prometheus 예시: CPU 사용률
        prom_data = query_prometheus('node_cpu_seconds_total')
        print(f"Prometheus result count: {len(prom_data)}")

        # Loki 예시: 특정 job 로그
        loki_data = query_loki('{job="rook-ceph/csi-rbdplugin"}')
        print(f"Loki result count: {len(loki_data)}")
        for entry in loki_data[:5]:  # 상위 5개 로그만 샘플 출력
            print(entry)

        time.sleep(5)

if __name__ == "__main__":
    main()

