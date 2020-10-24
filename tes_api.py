import requests
import json
with open('test_image/aron3.jpg', 'rb') as f:
    read_data = f.read()

files = {
    'file': read_data,
}

response = requests.post('http://api/caption/', files=files)
data = response.content.decode()
data = json.loads(data) 
print(data, type(data))