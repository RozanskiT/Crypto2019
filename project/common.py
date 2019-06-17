def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def is_veto(answers, p):
    l = 1
    for i in answers:
        l = l * i % p
    if l == 1:
        return False
    else:
        return True


HOST = 'localhost'
PORT = 2465
BUFF_SIZE = 1024
QUESTION = 'Are we voting for decreasing of taxes?'
