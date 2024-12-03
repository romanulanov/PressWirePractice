import httpx


def get_json(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        print(f'an error occurred while requesting {exc.request.url}')
        raise


def post_json(url, payload):
    try:
        response = httpx.post(url, json=payload)
        return response.json()
    except httpx.RequestError as exc:
        print(f'an error occurred while requesting {exc.request.url}')
        raise
