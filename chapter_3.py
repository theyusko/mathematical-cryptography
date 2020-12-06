from math import ceil, floor, sqrt, gcd
from sage.all import is_prime, euler_phi
from random import randint


def rsa_create_key(digits=309, p=None, q=None, e=65537):
    """
    :param digits: Digits of modulus N in RSA PKC
    :param q: prime q where N = p * q is modulus
    :param p: prime p where N = p * q is modulus
    :param e: gcd(e, (p-1)*(q-1)) = 1
    :return:
    """

    # For security N=p*q >= 1024 bits (308 digits)
    if p is None:
        if q is None:
            lenp = floor(digits/2)
            p = rand_prime(lenp)
            q = rand_prime(digits - lenp)
        else:
            p = rand_prime(digits - len(q))
    elif q is None:
        q = rand_prime(digits - len(p))

    # For RSA to be secure d >= N^(1/4), therefore e < N^(3/4)
    # if N is relatively large 2^16 + 1 = 65537 is good enough for e
    if e == 65537 and e >= (p-1)*(q-1):
        lenpq = ceil(len((p-1)*(q-1)) / 4)
        e = rand_prime(lenpq - 1) # e < N^(1/4)

    return p, q, e


def rsa_encrypt(m, N, e):
    """
    :param m: plaintext
    :param N: public modulus key
    :param e: public exponentiation key
    :return: ciphertext
    """
    return (m**e) % N


def rsa_decrypt(c, p, q, e):
    phi = euler_phi((p-1)*(q-1))

    d = pow(e, phi-1, (p-1)*(q-1))

    return pow(c, d, p*q)


def babystep_giantstep(g, h, p):
    """
    :param p: prime
    Solves g^x = h (modulo p).
    :return: x
    """
    # TODO: check if works with p not prime

    n = 1 + floor(sqrt(p-1))

    pows = {i: pow(g, i, p) for i in range(n+1)}  # create dict {e,g,g^2,...,g^n}
    pows2 = {j: ((h * pow(g, -n*j)) % p) for j in range(n+1)}  # create dict {h, h*g^(-n), h*g^(-2n),.. h*g^(-n^2)}

    # Find a match between two dicts
    for i,val in pows.items():
        for j, val2 in pows2.items():
            if val == val2:
                return i+j*n

    return None


def miller_rabin(a, n):
    # Checks if 'a' is a Miller-Rabin witness for compositeness of 'n'
    # TODO: Check if this works correctly
    if n == 2:
        return False
    if n % 2 == 0 or gcd(a, n) > 1:
        return True

    # Write n-1 = 2^k*q with q odd.
    k = 0; q = n - 1
    while q % 2 == 0:
        k += 1; q /= 2

    # Sage converts q & n to its own types. Convert back to use built-in pow
    q = int(q); n = int(n)
    l = pow(a, q, n)

    if l % n == 1:
        return False

    for i in range(k):
        if l % n == n-1:
            return False
        l = (l*l) % n

    return True


def rand_prime(digits=309):
    """
    :param digits: number of bits the prime should have
    :return: a prime
    """

    p = 0
    while is_prime(p) is False:  # Primality can also be checked with Rabin Miller test
        p = randint(10 ** (digits-1), 10 ** digits)
        if p % 2 == 0:
            p += 1

    return p



p,q,e = rsa_create_key(309,None,None,3)
print("p:"+ str(p) + "\tq:" + str(q) + "\te:" + str(e))
