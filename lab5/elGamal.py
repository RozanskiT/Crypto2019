#!/usr/bin/python3
# -*- coding: utf-8 -*-
from edwardCurve import EdwardCurve, pointEC
import random

"""
DESCRIPTION
El Gamal cryptosystem (<Gen,Enc,Dec>) over the Edward elliptic curve
"""

class ElGamal:

    def __init__(self,curve,g):
        self.curve = curve
        self.g = g
        self.ord = g.ord()
        # print(self.g ,self.ord)
        self.privKey = None
        self.publicKey = None
        self.publicKeyEnc = None

    def setPublicKey(self, publicKey):
        assert self.curve.checkIfPointOnCurve(publicKey)
        self.publicKeyEnc = publicKey

    def gen(self):
        self.privKey = random.randint(1, self.ord - 1)
        self.publicKey = self.privKey * self.g
        return self.publicKey

    def enc(self, message_point):
        assert self.curve.checkIfPointOnCurve(message_point) # Check if message point is on curve
        randInt = random.randint(1, self.ord - 1)  # can be bigger
        cipher = randInt * self.g, message_point + randInt * self.publicKeyEnc
        return cipher

    def dec(self,cipher):
        p1, p2 = cipher
        assert self.curve.checkIfPointOnCurve(p1)
        assert self.curve.checkIfPointOnCurve(p2)
        return p2 - p1*self.privKey

def main():
    d = 5
    p = 17

    ec = EdwardCurve(p,d)
    g = pointEC(7, 12, ec)

    eg1 = ElGamal(ec,g) # creating ElGamal system of first user
    publicKey = eg1.gen() # generating end announcing public Key
    print("Public key is {}".format(publicKey))

    eg2 = ElGamal(ec,g) # creating ElGamal system of second user
    eg2.setPublicKey(publicKey) # setting announced public key
    message = pointEC(12, 7,ec)
    print("Message is {}".format(message))
    cipher = eg2.enc(message)
    print("Cipher is {}".format(cipher))

    decrypted = eg1.dec(cipher) # First user decrypts message using his private key
    print("Decrypted message is {}".format(decrypted))

    assert message == decrypted

if __name__ == '__main__':
	main()
