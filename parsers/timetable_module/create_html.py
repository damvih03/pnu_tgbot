import requests


def create_html(url):
    headers = {}
    req = requests.get(url, headers=headers)
    with open("index.html", "w", encoding="UTF-8") as file:
        file.write(req.text)
    return
