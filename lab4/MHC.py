#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
DESCRIPTION
Implementation of Merkle-Hellman cryptosystem,
(see more:
Ralph Merkle and Martin E Hellman. Hiding information and signatures in trapdoor knapsacks.
Information Theory, IEEE Transactions on , 24(5):525 530, 1978
)

"""

import random
import numpy as np
import math

def getSuperincreasingSequence(n, nextInteger):
    seq = np.empty(n, dtype = np.int)
    s = 0
    for i in range(n):
        seq[i] = s + np.random.randint(1, nextInteger)
        s += seq[i]
    return seq, s

def getCoprime(q):
    r = q
    while math.gcd(q, r) != 1:
        r = np.random.randint(2, q)
    return r

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modInv(a, m):
    # https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist!')
    else:
        return x % m

class MerkleHellmanCryptosystem:

    def __init__(self, m, nextInteger = 10):
        self.m = m
        self.n = len(m)
        self.nextInteger = nextInteger

    def gen_key(self):
        seq, s = getSuperincreasingSequence(self.n, self.nextInteger)
        q = s + np.random.randint(1, self.nextInteger)
        r = getCoprime(q)
        pubKey = [r * seq % q for seq in seq]
        privKey = [seq, q, r]
        return pubKey, privKey

    def encrypt(self, pubKey):
        return sum([m * k for m, k in zip(self.m, pubKey)])

    def decrypt(self, cipher, privKey):
        seq, q, r = privKey
        s = modInv(r, q)
        c_prim = cipher * s % q
        decrypted = -np.ones(self.n, dtype = np.int)
        for i in range(self.n - 1, -1, -1):
            to_subtract = int(seq[i] <= c_prim)
            decrypted[i - self.n] = to_subtract
            c_prim -= seq[i] * to_subtract
        return decrypted

def main():
    N = 10
    plainText = np.random.randint(2,size = N)
    mhc = MerkleHellmanCryptosystem(plainText)
    pubKey, privKey = mhc.gen_key()
    ciphertext = mhc.encrypt(pubKey)
    dec = mhc.decrypt(ciphertext, privKey)
    assert np.all(plainText == dec)

if __name__ == '__main__':
	main()
