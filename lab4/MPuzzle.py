#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
DESCRIPTION

Implementation of Merkle Puzzle Cryptosystem
"""

import base64
import hashlib
from Crypto import Random
from Crypto.Random.random import randint
from Crypto.Cipher import AES
import numpy as np
import itertools
import time

class AESCipher:

    def __init__(self, key, mode = 'cbc'):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()
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

class puzzlesAES:
    constant = "stala"
    privateKey = "My private key"
    cipher = AESCipher(privateKey)

    def __init__(self, difficulty = 3):
        self.difficulty = difficulty

    def getPuzzles(self,N = 1000):
        puzzlesSet = []
        for  i in range(N):
            id = str(puzzlesAES.cipher.encrypt(str(i)))
            key = str(puzzlesAES.cipher.encrypt(str(id)))[:self.difficulty]
            puzzleCipher = AESCipher(key)

            encId = puzzleCipher.encrypt(id)
            encKey = puzzleCipher.encrypt(key)
            encConst = puzzleCipher.encrypt(puzzlesAES.constant)

            puzzlesSet.append([encId,encKey,encConst])

        return puzzlesSet

    def getKey(self,encId):
        choosenKey = str(puzzlesAES.cipher.encrypt(str(encId)))[:self.difficulty]
        return choosenKey

    def chooseRandomPuzzle(self, puzzlesSet, N):
        encID, encKey, CONST = puzzlesSet[Random.random.randint(0,N-1)]
        # solve that puzzle by brute force
        allPossibleKeys = itertools.product(bytes(range(0,256)),repeat = self.difficulty)
        for testKey in allPossibleKeys:
            mergedKey = ''.join(chr(c) for c in testKey)
            testAES = AESCipher(mergedKey)
            compare = None
            try:
                compare = testAES.decrypt(CONST)
            except:
                pass
            if puzzlesAES.constant == compare:
                id = testAES.decrypt(encID)
                key = testAES.decrypt(encKey)
                return key, id

class MerklePuzzleCryptosystem:

    def __init__(self, puzzles, noPuzzles = 100):

        self.noPuzzles = noPuzzles
        self.puzzles = puzzles
        self.puzzlesSet = None
        #---------------------------
        self.choosenId = None
        self.choosenKey = None
        self.choosenAESCipher = None
        #---------------------------

    def getPuzzlesSet(self):
        if self.puzzlesSet is None:
            self.puzzlesSet = self.puzzles.getPuzzles(self.noPuzzles)
        return self.puzzlesSet

    def findAndSetProperKey(self,encID):
        self.choosenKey = self.puzzles.getKey(encID)
        self.choosenAESCipher = AESCipher(self.choosenKey)

    def chooseRandomPuzzle(self,puzzlesSet):
        self.choosenKey, self.choosenId = self.puzzles.chooseRandomPuzzle(puzzlesSet,self.noPuzzles)
        self.choosenAESCipher = AESCipher(self.choosenKey)

    def getID(self):
        return self.choosenId

    def encrypt(self, message):
        return self.choosenAESCipher.encrypt(message)

    def decrypt(self, ciphertext):
        return self.choosenAESCipher.decrypt(ciphertext)

def main():
    # N = 100000
    N = int(2**24)
    difficulty = 2
    last = time.time()
    print("Running tests for N = {} and difficulty = {}".format(N,difficulty))

    puzzles_1 = puzzlesAES(difficulty = difficulty)
    mps_1 = MerklePuzzleCryptosystem(puzzles_1,N)

    puzzles_2 = puzzlesAES(difficulty = difficulty)
    mps_2 = MerklePuzzleCryptosystem(puzzles_2,N)

    puzzlesSet = mps_1.getPuzzlesSet()
    print("Generation of puzzlesSet takes = {:.1f} sec".format(time.time() - last))
    last = time.time()

    mps_2.chooseRandomPuzzle(puzzlesSet)
    print("Solving random puzzle = {:.1f} sec".format(time.time() - last))
    id = mps_2.getID()

    mps_1.findAndSetProperKey(id)

    #------------------------------
    message_1 = "Ala ma kota"
    ciphertext_1 = mps_1.encrypt(message_1)
    decrypted_1 = mps_2.decrypt(ciphertext_1)

    assert(message_1 == decrypted_1)

    message_2 = "Ala ma dwa koty"
    ciphertext_2 = mps_2.encrypt(message_2)
    decrypted_2 = mps_1.decrypt(ciphertext_2)

    assert(message_2 == decrypted_2)

    print("Test passed!")


if __name__ == '__main__':
	main()
