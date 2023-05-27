import time
import requests


def send_post_request():
    requests.post("http://127.0.0.1:8000/posts_results", data={"title": "send_request"})


while True:
    send_post_request()
    time.sleep(3600) # time till restart every x seconds
