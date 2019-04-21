#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import jks
import random
from Crypto.Cipher import AES
import base64
import hashlib
from Crypto import Random

class AESCipher:

    def __init__(self, key, mode = 'cbc'):
        self.bs = AES.block_size
        self.key = key
        if mode == 'ofb':
            self.mode = AES.MODE_OFB
        elif mode == 'cbc':
            self.mode = AES.MODE_CBC
        elif mode == 'ctr':
            self.mode = AES.MODE_CTR
        else:
            print("Accepted modes are: 'ofb', 'cbc'(Default), and 'ctr'")
            self.mode = AES.MODE_CBC

    def encrypt(self, raw):
        raw = raw.encode()
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        if self.mode == AES.MODE_CTR:
            cipher = AES.new(self.key, self.mode)
            nonce = cipher.nonce
            return base64.b64encode(nonce + cipher.encrypt(raw))
        else:
            cipher = AES.new(self.key, self.mode, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)

        if self.mode == AES.MODE_CTR:
            nonce = enc[:AES.block_size//2]
            cipher = AES.new(self.key, self.mode,nonce = nonce)
            return self._unpad(cipher.decrypt(enc[AES.block_size//2:])).decode('utf-8')
        else:
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, self.mode, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, data):
        length = 16 - (len(data) % 16)
        data += bytes([length])*length
        return data

    @staticmethod
    def _unpad(data):
        return data[:-data[-1]]

def encryptFile(inputFileName, outputFileName, key, mode):
    aes256c = AESCipher(key, mode)
    with open(inputFileName,'r') as f:
        plainText = f.read()
    ciphertext = aes256c.encrypt(plainText)
    with open(outputFileName,'wb') as f:
        f.write(ciphertext)


def decryptFile(inputFileName, outputFileName, key, mode):
    aes256c = AESCipher(key, mode)
    with open(inputFileName,'rb') as f:
        ciphertext = f.read()
    plainText = aes256c.decrypt(ciphertext)
    with open(outputFileName,'w') as f:
        f.write(plainText)

def encryptionOracle(inputFileName, key, mode):
    with open(inputFileName) as f:
        data = f.readlines()
    data = [l.rstrip() for l in data]

    aes256c = AESCipher(key, mode)
    ciphertexts = []
    for l in data:
        ciphertext = aes256c.encrypt(l)
        print(l)
        print(ciphertext)
        ciphertexts.append(ciphertext)
        print("# ========")
    return ciphertexts

def challenge(inputFileName,key,mode):
    with open(inputFileName) as f:
        data = f.readlines()
    data = [l.rstrip() for l in data]

    aes256c = AESCipher(key, mode)
    b = random.getrandbits(1)
    message_b = data[int(b)]
    ciphertext = aes256c.encrypt(message_b)
    print(ciphertext)
    return ciphertext


def tests():
    print("Start enc-dec tests")
    s = u"Ala ma kota"
    key = hashlib.sha256("Key".encode()).digest()
    # ======
    mode = 'cbc'
    print("Testing mode = {}".format(mode))
    aes256c = AESCipher(key, mode)
    ciphertext = aes256c.encrypt(s)
    plainText = aes256c.decrypt(ciphertext)
    assert(plainText == s)
    #-------
    mode = 'ofb'
    print("Testing mode = {}".format(mode))
    aes256c = AESCipher(key, mode)
    ciphertext = aes256c.encrypt(s)
    plainText = aes256c.decrypt(ciphertext)
    assert(plainText == s)
    #-------
    mode = 'ctr'
    print("Testing mode = {}".format(mode))
    aes256c = AESCipher(key, mode)
    ciphertext = aes256c.encrypt(s)
    plainText = aes256c.decrypt(ciphertext)
    assert(plainText == s)
    # ======
    print("TESTS done!!!")

def main():
    # Hasło do keystore - passwd
    # eg. call
    # python cryptoAES.py -i oracle.txt -o output.txt --mode tests --passwd passwd --keystore keystore.jceks --keyID aes256key
    #-------
    # Creating keystore
    # https://docs.servicenow.com/bundle/london-servicenow-platform/page/administer/edge-encryption/task/t_CreateEncryptionKeys.html
    #-------
    # In my case it was:
    # keytool -genseckey -alias aes256key -keyalg aes -keysize 256 -keystore keystore.jceks -storetype jceks
    parser = argparse.ArgumentParser(description='Program encrypts/decrypts selected files on disk.')

    parser.add_argument('--encmode', type = str)
    parser.add_argument('--mode', type = str)
    parser.add_argument('-i','--inputFileName',type = str)
    parser.add_argument('-o','--outputFileName',type = str)
    parser.add_argument('-k','--keystore',type = str)
    parser.add_argument('--keyID',type = str)
    parser.add_argument('-p','--passwd',type = str)

    args = parser.parse_args()

    if args.mode == 'tests':
        # python cryptoAES.py --mode tests
        tests()
        return

    keystore = jks.KeyStore.load(args.keystore, args.passwd)
    key = keystore.secret_keys[args.keyID].key

    if args.mode == 'challenge':
        # python cryptoAES.py -i challenge.txt --mode challenge --passwd passwd --keystore keystore.jceks --keyID aes256key --encmode ctr
        challenge(args.inputFileName,key,args.encmode)
    elif args.mode == 'oracle':
        # python cryptoAES.py -i oracle.txt --mode oracle --passwd passwd --keystore keystore.jceks --keyID aes256key --encmode ctr
        encryptionOracle(args.inputFileName,key,args.encmode)
    elif args.mode =='dec':
        # python cryptoAES.py -i outputEnc.bin -o outputDec.txt --mode dec --passwd passwd --keystore keystore.jceks --keyID aes256key --encmode cbc
        decryptFile(args.inputFileName,args.outputFileName,key,args.encmode)
    elif args.mode == 'enc':
        # python cryptoAES.py -i oracle.txt -o outputEnc.bin --mode enc --passwd passwd --keystore keystore.jceks --keyID aes256key --encmode cbc
        encryptFile(args.inputFileName,args.outputFileName,key,args.encmode)
    else:
        print("Accepted modes are: enc, dec, challenge, oracle and tests")


if __name__ == '__main__':
	main()
