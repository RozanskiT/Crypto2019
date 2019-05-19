#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Assignment 2.
Construct and implement an efficient statistical test that predicts (with
non-negligible probability) next bits of glibc’s random().
---------------------------
for details in glibc check:
    rand.c
    random.c
    random_r.c
    stdlib.h
"""
import random

def glibcPRGN(seed):
    """
    glibc random generator, based on:
    https://www.mathstat.dal.ca/~selinger/random/
    and
    https://github.com/qbx2/python_glibc_random/blob/master/glibc_prng.py
    """
    int32 = lambda x: x&0xffffffff-0x100000000 if x&0xffffffff>0x7fffffff else x&0xffffffff
    int64 = lambda x: x&0xffffffffffffffff-0x10000000000000000 if x&0xffffffffffffffff>0x7fffffffffffffff else x&0xffffffffffffffff

    r = [0] * 34
    r[0] = seed

    for i in range(1, 31):
        r[i] = int32(int64(16807 * r[i-1]) % 0x7fffffff)

        if r[i] < 0:
            r[i] = int32(r[i] + 0x7fffffff)

    for i in range(31, 34):
        r[i] = int32(r[i-31])

    for i in range(34, 344):
        r.pop(0)
        r.append(int32(r[2] + r[30]))

    while True:
        r.pop(0)
        r.append(int32(r[2] + r[30]))
        yield int32((r[-1]&0xffffffff) >> 1)

def getNextGlibcRandom(glibcRandomSequence):
    """
    With 75% gives correct next random
    """
    o1, o2 = glibcRandomSequence[-3], glibcRandomSequence[-31]
    return (o1+o2)%0x80000000

def testDistinguisher(sequenceLength, noTests=1000):
    num = 0.
    bits = [random.randint(0,1) for _ in  range(noTests)]

    for i, b in enumerate(bits):
        rng = glibcPRGN(random.randint(1,100*noTests))
        randomSequence = [ next(rng) for _ in range(sequenceLength)]
        nextVal = 0
        if b: # use
            nextVal = next(rng)
        else:
            nextVal = random.randint(0,1)
        ifGlibCRAND = True
        try:
            ifGlibCRAND = distinguisher(randomSequence, nextVal)
        except:
            ifGlibCRAND = -1
        if ifGlibCRAND == b:
            num += 1.
    return num/noTests * 100.

def distinguisher(randomSequence, nextVal):
    guess = getNextGlibcRandom(randomSequence)
    return guess == nextVal

def main():
    sequenceLength = 34
    numberOfTests = 1000
    pc = testDistinguisher(sequenceLength, numberOfTests)
    print("Distinguisher accuracy = {:.3f}".format(pc))

if __name__ == '__main__':
	main()
