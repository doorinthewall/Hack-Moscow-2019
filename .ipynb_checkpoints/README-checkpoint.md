# Hack-Moscow-2019

## Как стартовать
```bash
gunicorn --config gunicorn_config.py 'server:get_app()'
```

## Как обратиться?
```python
import requests

params = {
    'latitude': 20.0,
    'longitude': 25.6,
    'n': 3,
}
response = requests.get('http://0.0.0.0:5000/get_recommendation', params=params, proxies={'http': ''})
response.text
```