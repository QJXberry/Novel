# coding:utf8
from Crypto.Hash import MD5


def md5_encrypt(s):
    md5 = MD5.new(s)
    return md5.hexdigest()


def re_md5_encrypt(s):
    return md5_encrypt(s)[::-1]

if __name__ == '__main__':
    pass
