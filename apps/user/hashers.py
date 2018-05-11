from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth.hashers import mask_hash
from django.contrib.auth.hashers import OrderedDict
import hashlib


class MD5Password(MD5PasswordHasher):
    algorithm = "md5_no_salt"

    def encode(self, password, salt):
        assert password is not None
        hash = hashlib.md5(password).hexdigest()
        return hash

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, '')
        return encoded == encoded_2

    def safe_summary(self, encoded):
        return OrderedDict([
            (_('algorithm'), self.algorithm),
            (_('salt'), ''),
            (_('hash'), mask_hash(hash)),
        ])