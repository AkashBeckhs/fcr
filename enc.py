import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]


class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        #iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt( raw )).decode('utf-8')

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        #v = enc[:16]
        cipher = AES.new(self.key, AES.MODE_ECB )
        return unpad(cipher.decrypt( enc)).decode('utf-8')


