from requests import post

print('токен',
      post(
          'http://localhost:8080/api/auth',
          json={'username': 'gamba232', 'password': 'gamba232'}).json())

token = post('http://localhost:8080/api/auth',
             json={'username': 'gamba232', 'password': 'gamba232'}).json()[
    'token']

print(post('http://localhost:8080/api/task',
           json={'token': token, 'name': 'П',
                 'date': '2018-01-01 12:30:12'}).json())
