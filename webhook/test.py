import requests
import json

url = "https://hooks.slack.com/triggers/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"
headers = { "Content-Type" : "application/json" }
body = { "message" : "테스트용 메시지" }

res = requests.post(url, headers=headers, data=json.dumps(body))

print("status :", res.status_code)
print("Response Body :", res.text)
