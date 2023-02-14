from datetime import date
import requests

response = requests.get(
    "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/hour/2023-01-09/2023-01-09?adjusted=true&sort=asc&limit=3600&apiKey=qxopP6_J4g7SNqKAFlq8lqEFwufYg80L"
)

print(response.json())

'''
{"action":"auth","params":"PKKZSVR4ICWFB6YOHU04"}
'''
