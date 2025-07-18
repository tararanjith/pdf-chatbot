import requests

url = "http://localhost:5000/chat"
question = "what are the skills of anushri"

response = requests.post(url, json={"query": question})

print("Status Code:", response.status_code)
print("Response:", response.json())
