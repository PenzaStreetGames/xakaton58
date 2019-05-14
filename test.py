from requests import post

print('токен', post('http://localhost:8080/api/auth', json={'username': 'gamba2332',
                                                         'password': 'gamba232'}).json())