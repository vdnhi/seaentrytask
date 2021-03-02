import requests
import json
import random
import time


BLOCK_SIZE = 16
MAX_USER = 1000000
HOST = '127.0.0.1:8000'

def main():
    start_time = time.time()
    count = 0
    while True:
        index = random.randint(0, 1000000)
        username = 'user{}'.format(index)
        response = requests.post('http://{}/user/prelogin/'.format(HOST),
                json={'username': username})
        if time.time() - start_time >= 1:
            print(count)
            count = 0
            start_time = time.time()
        count += 1

if __name__ == '__main__':
    main()

