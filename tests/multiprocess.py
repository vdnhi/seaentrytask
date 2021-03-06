from multiprocessing import Pool
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

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

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


def api_call(id):
    username = 'user{}'.format(id)
    response = requests.post(
        'http://{}/api/user/prelogin/'.format(HOST), json={'username': username})
    data = response.json()
    if response.status_code == 200 and data['error'] is None:
        password = encrypt(username, data['data']['key'].encode('utf-8'))
        response = requests.post('http://{}/api/user/login/'.format(HOST),
                                 json={'username': username, 'password': password})
        data = response.json()
        if response.status_code == 200 and data['error'] is None:
            return True


def main():
    pool_size = 42
    print('Testing with pool_size = {}'.format(pool_size))
    for i in range(5):
        tic = time.time()
        p = Pool(pool_size)
        p.map(api_call, range(500 * i, 500 * (i + 1)))
        toc = time.time()
        print(500*i, 500 * (i+1), toc - tic)


if __name__ == '__main__':
    main()
