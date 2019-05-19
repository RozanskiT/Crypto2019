#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
DESCRIPTION
Assignment 1.
Construct and implement an efficient statistical test that predicts (with
non-negligible probability) next bits of linear congruencial generator.
"""
import numpy as np
import random

def LCG(modulus,multiplier,increment,seed):
    """
    Linear congruential generator,
    https://en.wikipedia.org/wiki/Linear_congruential_generator
    """
    while True:
        yield seed
        seed = (multiplier*seed + increment) % modulus

def crackLCG(lcgSequence):
    """
    Learned from:
    https://tailcall.net/blog/cracking-randomness-lcgs/
    """
    try:
        modulus = findModulus(lcgSequence)
        multiplier = findMultiplier(lcgSequence, modulus)
        increment = findIncrement(lcgSequence, modulus, multiplier)
    except:
        return 0, 0, 0
    return modulus, multiplier, increment

def findModulus(lcgSequence):
    from math import gcd
    from functools import reduce
    diffs = [s1 - s0 for s0, s1 in zip(lcgSequence, lcgSequence[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus

def findMultiplier(lcgSequence, modulus):
    multiplier = (lcgSequence[2] - lcgSequence[1]) * modinv(lcgSequence[1] - lcgSequence[0], modulus) % modulus
    return multiplier

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    # g = b*x + n*y
    g, x, y = egcd(b, n)
    if abs(g) != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return g*x % n

def findIncrement(lcgSequence, modulus, multiplier):
    return (lcgSequence[1] - lcgSequence[0]*multiplier) % modulus


def testAccuracy(lcgGenerator, numberOfTests, sequenceLength, generatorValues):
    """
    Procedure tests accuracy of finding LCG parameters
    """
    num = 0
    for _ in range(numberOfTests):
        lcgSequence = [next(lcgGenerator) for _ in range(sequenceLength)]
        num += np.array_equal(generatorValues, crackLCG(lcgSequence))
    return num*100. / numberOfTests

def testDistinguisher(lcgGenerator, modulus, sequenceLength, noTests=1000):
    num = 0.
    bits = [random.randint(0,1) for _ in  range(noTests)]
    for b in bits:
        nextVal = 0
        randomSequence = [next(lcgGenerator) for _ in range(sequenceLength)]
        if b: # use
            nextVal = next(lcgGenerator)
        else:
            nextVal = random.randint(1,modulus)
        ifLCG = True
        try:
            ifLCG = distinguisher(randomSequence,nextVal)
        except:
            ifLCG = -1
        if ifLCG == b:
            num += 1.
    return num/noTests * 100.

def distinguisher(randomString, nextVal):
    modulus, multiplier, increment = crackLCG(randomString)
    testValue = (multiplier*randomString[-1] + increment) % modulus #LCG
    return testValue == nextVal

def main():
    import random
    # MMIX by Donald Knuth
    modulus = 2**64
    multiplier = 6364136223846793005
    increment = 1442695040888963407
    # seed = 10
    seed = random.randint(1, 1000)
    LCGGenerator = LCG(modulus,multiplier,increment,seed)
    # Get n numbers from generator
    sequenceLength = 10
    makeTest = True
    if makeTest: # test accuracy of distinguisher in %
        pc = testDistinguisher(LCGGenerator, modulus, sequenceLength, noTests = 1000)
        print("Distinguisher accuracy = {:.3f}".format(pc))
    else:
        numberOfTests = 10000
        acc = testAccuracy(LCGGenerator,numberOfTests,sequenceLength,(modulus,multiplier,increment))
        print("Accuracy in {} tests is : {:.2f}%".format(numberOfTests,acc))


if __name__ == '__main__':
	main()
