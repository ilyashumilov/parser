import requests


response = requests.get('http://127.0.0.1:8000/?query=Macbook%20Pro')

if __name__ == '__main__':
    print(response.text)