import requests

with open('test_image/aron3.jpg', 'rb') as f:
    read_data = f.read()

files = {
    'file': read_data,
}

response = requests.post('http://52.188.166.61/caption/', files=files)
print(response.content.decode())