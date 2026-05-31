import httpx

r = httpx.get('http://localhost:8000/api/news?category=russia', timeout=5)
print('Russia category:', r.json()['total'], 'items')

r = httpx.get('http://localhost:8000/api/news?category=private', timeout=5)
print('Private category:', r.json()['total'], 'items')

r = httpx.get('http://localhost:8000/api/news?category=science', timeout=5)
print('Science category:', r.json()['total'], 'items')

r = httpx.get('http://localhost:8000/api/news', timeout=5)
print('Total all:', r.json()['total'], 'items')
