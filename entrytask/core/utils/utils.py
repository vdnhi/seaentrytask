import base64
import hashlib
import string
from hashlib import md5
import random
from Crypto.Cipher import AES
from django.core.cache import cache
from django.db import DatabaseError
from jsonschema import ValidationError

from core.models import User, UserRoleMapping

BLOCK_SIZE = 16


def string_generator(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


# Reference: https://stackoverflow.com/questions/36762098/how-to-decrypt-password-from-javascript-cryptojs-aes
# -encryptpassword-passphras/36780727

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length) * length).encode()


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


def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))


def hasher(password, salt):
    return hashlib.sha256(password + salt).hexdigest()


def validate_user(username, password, input_role):
    try:
        user = User.objects.filter(username=username).first()
        role = UserRoleMapping.objects.filter(user_id=user.id).first()
        return user, role.role_id, user.salted_password == hasher(password, user.salt) and input_role == role.role_id
    except DatabaseError as exception:
        print(exception)
        return -1, -1, False


def validate_token(token, user_id):
    if cache.get(token) is None:
        raise ValidationError('')
    cached_data = cache.get(token)

    if user_id != cached_data['id']:
        raise ValidationError('')

