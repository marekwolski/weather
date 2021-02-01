import requests, json

url = 'http://192.168.1.17:8080/json'
r = requests.get(url)
stats = json.loads(r.content)
print(stats)
print('Temperature is ', f"{stats['temp']:.1f}")
print('Pressure is ', f"{stats['pressure']:.1f}")
print('Humidity is ', f"{stats['humidity']:.1f}")
