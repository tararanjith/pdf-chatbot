import requests

url = "http://127.0.0.1:5000/upload"
file_path = "C:/Users/tarar/Downloads/yourfile.pdf"  # Replace with your actual PDF filename

try:
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        response = requests.post(url, files=files)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
