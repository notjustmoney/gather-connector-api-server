import requests


def client():
    credentials = {"username": "mjmj0217@naver.com", "password": "12345678"}
    request_url = 'http://127.0.0.1:8000/api/auth/token/'
    response = requests.post(request_url, data=credentials)

    print('Status code: ', response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == '__main__':
    client()
