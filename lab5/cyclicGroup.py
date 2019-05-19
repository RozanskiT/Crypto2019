#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION
Cyclic group implementation
http://ecchacks.cr.yp.to/edwardsadd.html
"""
def Z(p):
    class Z:
        def __init__(self, x):
            self.x = x % p

        def __str__(self):
            return "{}(mod{})".format(self.x,p)

        def __eq__(self, b):
            return self.x == b.x

        def __ne__(self, b):
            return self.x != b.x

        def __mod__(self,b):
            assert b == p
            return self.x

        def __add__(self, b):
            return Z(self.x + b.x)

        def __sub__(self, b):
            return Z(self.x - b.x)

        def __neg__(self):
            return Z(-self.x)

        def __mul__(self, b):
            return Z(self.x * b.x)

        def __truediv__(self, b):
            return self * Z(pow(b.x, p - 2, p))

        def __repr__(self):
            return str(self.x)

    return Z

def main():
    Z7 = Z(7)
    a = Z7(3)
    b = Z7(4)
    one = Z7(1)
    two = Z7(2)

    assert a != b
    assert a == a
    assert a+two == Z7(5)
    assert one/a == Z7(5)


if __name__ == '__main__':
	main()
