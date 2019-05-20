#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
DESCRIPTION
Assignment 2

Implement algorithms (RC4, RC4-RS, RC4-SST) and test the quality
of generated random bits depending on the parameters:
1. RC4(N, N)-mdrop[D]
2. RC4-RS(N,2N log N )-mdrop[D]
3. RC4-SST(N)-mdrop[D]

Repeat experiments for different values of
N = 16, 64, 246
key lengths: 40, 64, 128
D = 0, 1, 2, 3 .
"""
import sys, os
import math
import itertools

# --------------------  RC4s
def rc4(key, n, t, d):
    return _rc4(key,n,t,d,ksa)

def rc4RS(key, n, t, d):
    return _rc4(key,n,t,d,ksa_rs)

def rc4SST(key, n, t, d):
    return _rc4(key,n,t,d,ksa_sst)

def _rc4(key, n, t, d, ksaAlg):
    s = ksaAlg(key, n, t)
    return prga(s, n, d)
# --------------------  KSAs
def ksa(key, n, t):
    num_key = str2num(key)
    key_length = len(num_key)
    s = list(range(n))
    j = 0
    for i in range(t):
        j = (j + s[i % n] + num_key[i % key_length]) % n
        s[i % n], s[j] = s[j], s[i % n]
    return s

def ksa_rs(key, n, t):
    s = list(range(n))
    bit_key = str2bin(key)
    l = len(bit_key)
    for r in range(t):
        top = []
        bot = []
        for i in range(n):
            if bit_key[(r * n + i) % l] == '0':
                top.append(s[i])
            else:
                bot.append(s[i])
        top.extend(bot)
        s = top.copy()
    return s

def ksa_sst(key, n, t):
    num_key = str2num(key)
    key_length = len(num_key)
    s = list(range(n))

    marked_lst = [False for _ in range(n)]
    marked_lst[-1] = True
    marked_num = 1
    j = n
    i = 0
    while marked_num < n:
        i = i % n
        j = (j + s[i % n] + num_key[i % key_length]) % n
        swap(s, i, j)
        if marked_num < n / 2:
            if not marked_lst[j] and not marked_lst[i]:
                marked_lst[j] = True
                marked_num += 1
        else:
            if (not marked_lst[j] and marked_lst[i]) or (not marked_lst[j] and i == j):
                marked_lst[j] = True
                marked_num += 1
        swap(marked_lst, i, j)
        i += 1
    return s

# --------------------  PRGA
def prga(S, n, d): # Output pseudo-random bytes from S
    i = j = 0
    tmp_d = 0
    while True:
        tmp_d += 1
        i = (i + 1) % n
        j = (j + S[i]) % n
        swap(S, i, j)
        z = S[(S[i] + S[j]) % n]
        if tmp_d > d:
            tmp_d = 0
            yield z

def swap(a, i, j):
    a[i], a[j] = a[j], a[i]

# -------------------- OTHER

def str2num(lst):
    return [ord(x) for x in lst]


def str2bin(key):
    return ''.join(format(ord(x), '08b') for x in key)

def num2hex(lst):
    return ''.join([format(x, '02X') for x in lst])

fullKey =   "q6kDWzk4iSFu3YsDo8zM"+\
            "cnKahLP5QecVZ7pPkJXf"+\
            "tv6MarWUs4iMiAvzlsC8"+\
            "YJXuBsverlvG8Xv0n9ql"+\
            "FDbw5Quhk803aG0eEH4l"+\
            "rlk0m5yeF2HAMExqTknR"+\
            "xG3nq9gE7nTpYyEcyAS8"+\
            "5yce0frNvVOFcwajM2g0"+\
            "iTmxVyCXiazDjAaf3vVT"+\
            "eC5zrg3DQiOReYlo6jxi"

# -------------------- TESTS

def testRC4():
    key = fullKey[:40]
    stream = rc4(key, 16, 16, 0)
    output = [bytes([next(stream)]) for i in range(10 ** 1)]
    print(output)

def testrc4RS():
    key = fullKey[:40]
    stream = rc4RS(key, 16, 16, 0)
    output = [bytes([next(stream)]) for i in range(10 ** 1)]
    print(output)

def testrc4SST():
    key = fullKey[:40]
    stream = rc4SST(key, 16, 16, 0)
    output = [bytes([next(stream)]) for i in range(10 ** 1)]
    print(output)

# Generate files for dieharder input
def createTestFiles(directory,n,kl,d,a):
    name = "{}_n{}_k{}_d{}.dat".format(a.__name__,n,kl,d)
    fileName = os.path.join(directory,name)
    print(fileName)
    n_numbers = n
    t = n
    if a == rc4RS:
        t = int(2 * n * math.log(n))
    with open(fileName, 'w') as f:
        stream = a(fullKey[:kl], n, t, d)
        for i in range(n_numbers):
            val = num2hex([next(stream)])
            f.write(val + '\n')

def main():
    tests = False
    if tests:
        testRC4()
        testrc4RS()
        testrc4SST()
    # -------------------
    short = True
    if short:
        N = [64]
        keyLen = [64]
        drop = [2]
        directory = "shortResults"
    else:
        N = [16, 64, 246]
        keyLen = [40, 64, 128]
        drop = [0, 1, 2, 3]
        directory = "allResults"
    # -------------------
    algorithm = [rc4,rc4RS,rc4SST]
    work = True
    if work:
        for n, kl, d, a in itertools.product(N,keyLen,drop,algorithm):
            createTestFiles(directory,n,kl,d,a)

if __name__ == '__main__':
	main()
