#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA

"""
DESCRIPTION
1. Reading Public RSA key and output n, e
"""

def readRSAPublicKey(publicKeyFileName):
    key = RSA.importKey(open(publicKeyFileName).read())
    return key.n, key.e

def main():
    publicKeyFileName = "cakey.pem"
    n,e = readRSAPublicKey(publicKeyFileName)
    print(f"RSA: n = {n}, e = {e}")


if __name__ == '__main__':
	main()
