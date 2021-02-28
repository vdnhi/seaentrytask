import requests
import json
from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5
import time


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


HOST = '172.16.230.130'

def main():
    start_time = time.time()
    prelogin_fail = 0
    login_fail = 0
    count_ok = 0
    for index in range(500):
        username = 'user{}'.format(index)
        response = requests.post('http://{}/user/prelogin/'.format(HOST),
                json={'username': username})

        if response.status_code == 200:
            data = response.json()
            password = encrypt(username, data['key'].encode('utf-8'))
            response = requests.post('http://{}/user/login/'.format(HOST),
                    json={'username': username, 'password': password, 'role': 1})
            if response.status_code == 200:
                count_ok += 1
            else:
                login_fail += 1
        else:
            prelogin_fail += 1

    print('Done in {} seconds'.format(time.time() - start_time))
    print("Ok: {}".format(count_ok))
    print("Login fail: {}".format(login_fail))
    print("Prelogin fail: {}".format(prelogin_fail))


if __name__ == '__main__':
    main()

