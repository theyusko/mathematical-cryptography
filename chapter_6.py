from math import ceil, floor, sqrt, gcd, exp, log
from sage.all import is_prime, euler_phi, EllipticCurve, GF
from random import randint


def double_and_add(P, E, n):
    """
    :param P: a point in E(F(p))
    :param E: elliptic curve
    :param n: exponent >1
    :return: n*P
    """
    Q = P; R = 0

    while n > 0:
        if n % 2 == 1:
            if R == 0:
                R = Q
            else:
                R = R+Q
        Q = 2*Q
        n = floor(n/2)

    return R


def funct():
    return
