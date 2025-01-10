import requests

response  = requests.api.post('http://localhost:8080/api/v1/users/login', 
    headers= {
        'Content-Type': 'application/json'
    },
    json={
    'username': 'chatuba',
    'password': 'a$$word'
})

print(response)