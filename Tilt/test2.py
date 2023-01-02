import requests
import json

url = "http://hub.local:8080/tilt/setdata"


payload = json.dumps([
  100,
  1.098
])
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'session=b94f5317-5e9a-42fe-8222-f91c02b62bd5'
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.text)