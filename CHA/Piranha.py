import sys

from .CHAF import *
import secrets
from .Modes import *
class Piranha:
    ECB = 0
    CBC = 1
    CTR = 2

    BlockSize = 64

    @staticmethod
    def repeated_key_xor(plain_text, key):
        pt = plain_text
        len_key = len(key)
        encoded = []

        for i in range(0, len(pt)):
            encoded.append(pt[i] ^ key[i % len_key])
        return bytes(encoded)

    def __init__(self, key, mode: int, *args, **kwargs):
        self.key = key
        self.mode = mode
        if mode == Piranha.CTR or mode == Piranha.CBC:
            if 'iv' not in kwargs.keys():
                self.iv = secrets.token_hex(9)[:16].encode()
            else:
                self.iv = kwargs['iv']
        self.args = args
        self.kwargs = kwargs


    @staticmethod
    def split_nth(n: int, line: str):
        return [line[i:i + n] for i in range(0, len(line), n)]

    @staticmethod
    def pad(data: bytes, blockSize=None):
        if blockSize is None: blockSize = Piranha.BlockSize
        return PKCS7(blockSize).pad(data)

    @staticmethod
    def unpad(data: bytes, blockSize=None):
        if blockSize is None: blockSize = Piranha.BlockSize
        return PKCS7(blockSize).unpad(data)

    def encrypt(self, data: bytes, func=None):
        if func is None: func = FeistelN.fRAB_with_nonce(self.key, rep=2)
        if self.mode == Piranha.CTR:
            dataList = Piranha.split_nth(self.BlockSize, data)
            times = len(dataList)
            encrypted = []
            nonce: bytes
            for i in range(times):
                bytesI = i.to_bytes(i.bit_length(), sys.byteorder)
                nonce = self.iv + bytesI
                encryptedNonce = FeistelN().DE(nonce, 8, func, 'e', 's')
                encrypted.append(encryptedNonce)
            out = [Piranha.repeated_key_xor(Piranha.repeated_key_xor(dataList[i], c), self.key) for i, c in enumerate(encrypted)]
            return b''.join(out)
        if self.mode == Piranha.ECB:
            return FeistelN().DE(data, 8, func, 'e', 's')
        if self.mode == Piranha.CBC:
            dataList = Piranha.split_nth(self.BlockSize, data)
            times = len(dataList)
            encrypted = []
            nextXOR = self.iv
            for i in range(times):
                xoredData = Piranha.repeated_key_xor(dataList[i], nextXOR)
                encryptedData = FeistelN().DE(xoredData, 8, func, 'e', 's')
                encrypted.append(encryptedData)
                nextXOR = encryptedData
            return b''.join(encrypted)

    def decrypt(self, cipher: bytes, func=None):
        if func is None: func = FeistelN.fRAB_with_nonce(self.key, rep=2)
        if self.mode == Piranha.CTR: return self.encrypt(cipher, func)
        if self.mode == Piranha.ECB:
            return FeistelN().DE(cipher, 8, func, 'd', 's')
        if self.mode == Piranha.CBC:

            dataList = Piranha.split_nth(self.BlockSize, cipher)
            times = len(dataList)
            decrypted = []
            nextXOR = self.iv
            for i in range(times):
                decryptedData = FeistelN().DE(dataList[i], 8, func, 'd', 's')
                xored = Piranha.repeated_key_xor(decryptedData, nextXOR)
                decrypted.append(xored)
                nextXOR = dataList[i]
            return b''.join(decrypted)
class PKCS7(object):
    def __init__(self, block_size):
        self.block_size = block_size

    def pad(self, string):
        padding_number = self.block_size - len(string) % self.block_size
        if padding_number == self.block_size:
            return string
        padding = chr(padding_number).encode() * padding_number
        return string + padding

    def unpad(self, string):
        if not string: return string
        if len(string) % self.block_size:
            raise TypeError('string is not a multiple of the block size.')
        padding_number = string[-1]
        if padding_number >= self.block_size:
            return string
        else:
            if all(padding_number == c for c in string[-padding_number:] ):
                return string[0:-padding_number]
            else:
                return string