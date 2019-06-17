#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA

"""
DESCRIPTION
1. Creating private key from RSA public key factored with MSieve
"""

def egcd(a, b):
    """Extended Euclidean algorithm"""
    """https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm"""
    x,y,u,v = 0,1,1,0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b,a,x,y,u,v = a,r,u,v,m,n
    return b, x, y

def modinv(e, m):
    """Modular multiplicative inverse"""
    """https://en.wikipedia.org/wiki/Modular_multiplicative_inverse"""
    g, x, y = egcd(e, m)
    if g != 1:
        return None
    else:
        return x % m

def pqe2rsa(p, q, e):
    """Generate an RSA private key from p, q and e"""
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    key_params = (n, e, d, p, q)
    priv_key = RSA.construct(key_params)
    return priv_key.exportKey()


def main():
    p = 1524938362073628791222322453937223798227099080053904149
    q = 1385409854850246784644682622624349784560468558795524903
    e = 65537
    crackedPrivKey = "crackedGrade/cracked_cakey.pem"

    privKey = pqe2rsa(p, q, e)
    print(privKey)
    with open(crackedPrivKey, "wb") as fs:
        fs.write(privKey)


if __name__ == '__main__':
	main()
