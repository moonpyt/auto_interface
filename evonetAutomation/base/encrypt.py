# -*- coding: utf-8 -*-
from CryptoLibrary import CryptoLibrary


class Encrypt(object):
    '''
    加解密功能
    '''

    def decrypt(self, encrypt_data):
        # 解密
        decrypt_data = CryptoLibrary().get_decrypted_text(encrypt_data)
        return decrypt_data


import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad


class Aesecb(object):
    def __init__(self, key):
        self.key = key
        self.MODE = AES.MODE_ECB
        self.BS = AES.block_size

    # str不是16的倍数那就补足为16的倍数
    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    # 加密
    def encrypt(self, _text):
        # 初始化加密器
        aes = AES.new(Aesecb.add_to_16(self.key), self.MODE)
        encrypted_text = aes.encrypt(pad(_text.encode('utf-8'), self.BS))
        return encrypted_text.hex()

    # 解密
    def decrypt(self, text_):
        # 初始化加密器
        if len(text_) < 33:
            raise Exception('非aes ecb 加密内容,无法解析')
        decode = binascii.a2b_hex(text_)
        aes = AES.new(self.add_to_16(self.key), self.MODE)
        decrypted_text = aes.decrypt(decode)
        return unpad(decrypted_text, self.BS).decode('utf-8')


if __name__ == '__main__':
    ae = Aesecb("")
    encrypt_text = ""
    encrypt_result = ae.encrypt(encrypt_text)
    print(encrypt_result)
    decrypt_text = encrypt_result
    decrypt_result = ae.decrypt(decrypt_text)
    print(decrypt_result)
