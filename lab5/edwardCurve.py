#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cyclicGroup import Z
"""
DESCRIPTION
Implementation of Edward Curve arithmetics
"""

class EdwardCurve:

    def __init__(self,p,d):
        """ x**2 + y**2 = 1 + d * x**2 * y**2 (mod p) """
        self.p = p
        self.Zp = Z(p)
        self.d = self.Zp(d)
        self.one = self.Zp(1)

    def ifPointOnCurve(self,x,y):
        x = self.Zp(x)
        y = self.Zp(y)
        assert (x * x + y * y) == (self.one + self.d * x * x * y * y)
        return x, y

    def checkIfPointOnCurve(self,p):
        return self.ifPointOnCurve(p.x,p.y)

    def __eq__(self, b):
        return (self.p == b.p) & (self.d == b.d)

class pointEC:

    def __init__(self, x, y, EC):
        """ Implementation of Edward Curve point """
        self.x, self.y = EC.ifPointOnCurve(x, y)
        self.EC = EC

    def __str__(self):
        return "({}, {})(mod{})".format(self.x.x, self.y.x, self.EC.p)

    def __repr__(self):
        return "({}, {})(mod{})".format(self.x.x, self.y.x, self.EC.p)

    def __eq__(self, b):
        return (self.x == b.x) & (self.y == b.y) & (self.EC == b.EC)

    def __ne__(self, b):
        return not ((self.x == b.x) & (self.y == b.y) & (self.EC == b.EC))

    def __add__(self, b):
        assert self.EC == b.EC
        x1, y1 = self.x, self.y
        x2, y2 = b.x, b.y
        x3 = (x1 * y2 + y1 * x2) / (self.EC.Zp(1) + self.EC.d * x1 * y1 * x2 * y2)
        y3 = (y1 * y2 - x1 * x2) / (self.EC.Zp(1) - self.EC.d * x1 * y1 * x2 * y2)
        return pointEC(x3, y3, self.EC)

    def __mul__(self, scalar):
        if isinstance(scalar, self.__class__):
            assert False
        else:
            return self.scalarMul(scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __neg__(self):
        return pointEC(-self.x,self.y,self.EC)

    def __sub__(self,b):
        return self.__add__(-b)

    def scalarMul(self,scalar):
        if scalar == 0:
            return pointEC(0,1,self.EC)
        if scalar == 1:
            return self
        P = self.scalarMul(scalar // 2)
        P = P + P
        if scalar % 2:
            P = P + P
        return P

    def ord(self):
        """
        Return order of point which is minimum ord that:
        ord * point == 1 (1 on curve is (0,1))
        """
        one = pointEC(0,1,self.EC)
        assert self != one
        for i in range(2, self.EC.p):
            if i*self == one:
                return i
        return 1

def main():
    p = 1009
    d = -11
    ec = EdwardCurve(p,d)
    P1 = pointEC(7,415,ec)
    P2 = pointEC(23,487,ec)
    print(P1 + P2)
    # output: (944, 175)

if __name__ == '__main__':
	main()
