from threading import Thread
from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5
import requests
import json
import time


HOST = '172.16.230.130'
BLOCK_SIZE = 16


def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))


def process_id(id):
    username = 'user{}'.format(id) 
    response = requests.post('http://{}/user/prelogin/'.format(HOST),
            json={'username': username})
    if response.status_code == 200:
        data = response.json()
        password = encrypt(username, data['key'].encode('utf-8'))
        response = requests.post('http://{}/user/login/'.format(HOST),
                    json={'username': username, 'password': password, 'role': 1})
        if response.status_code == 200:
            return True

    return False


def process_id_range(id_range, store=None):
    """process a number of ids, storing the results in a dict"""
    if store is None:
        store = {}
    for id in id_range:
        store[id] = process_id(id)
    return store

def threaded_process(nthreads, id_range):
    """process the id range in a specified number of threads"""
    store = {}
    threads = []
    # create the threads
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t = Thread(target=process_id_range, args=(ids,store))
        threads.append(t)
    
    # start the threads
    [ t.start() for t in threads ]
    # wait for the threads to finish
    #[ t.join() for t in threads ]
    return store


def main():
    id_range = range(500)
    tic = time.time()
    reference = process_id_range(id_range)
    reftime = time.time() - tic
    print(1, reftime)

    nlist = [1,2,4,8,16,32,64, 128, 256]
    tlist = [reftime]
    for nthreads in nlist[1:]:
        tic = time.time()
        ans = threaded_process(nthreads, id_range)
        toc = time.time()
        print(nthreads, toc-tic)
        tlist.append(toc-tic)

if __name__ == '__main__':
    main()
