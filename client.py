import requests
import json
import jwt
import time

url = "http://localhost:5000/users"

SECRET_KEY = "my_secret_key"
current_time = int(time.time())
payload = {"user_id":"123","timestamp":current_time}
valid_token = jwt.encode({'user_id':"123", 'timestamp': current_time}, SECRET_KEY, algorithm = 'HS256')
headers ={
    'Content-Type' : 'application/json',
    'auth' : valid_token
}

response = requests.request("GET",url, headers = headers, json = payload)

print(response.text)