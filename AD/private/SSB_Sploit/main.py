import requests

r = requests.post('http://localhost:8500/index.php?id=578', json={'method': 'updatePassword', 'password': '3333333334'}, cookies={'PHPSESSID': '1a9752050fec049062fe4b953b3dac10'})
print(r.text)