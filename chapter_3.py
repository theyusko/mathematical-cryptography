from math import ceil, floor, sqrt, gcd
from sage.all import is_prime, euler_phi
from random import randint


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
            p = rand_prime(digits - len(str(q)))
    elif q is None:
        q = rand_prime(digits - len(str(p)))

    # For RSA to be secure d >= N^(1/4), therefore e < N^(3/4)
    # if N is relatively large 2^16 + 1 = 65537 is good enough for e
    if gcd(e, (p - 1) * (q - 1)) != 1 or (e == 65537 and e >= (p - 1) * (q - 1)):
        lenpq = ceil(len(str((p - 1) * (q - 1))) / 4)
        for i in range(1, 10 ** lenpq):
            if gcd(2*i + 1, (p - 1) * (q - 1)) == 1:
                break
        e = 2*i + 1

    return p, q, e


def rsa_encrypt(m, N, e):
    """
    :param m: plaintext
    :param N: public modulus key
    :param e: public exponentiation key
    :return: ciphertext
    """
    return pow(m, e, N)


def rsa_decrypt(c, p, q, e):
    """
    :param c: ciphertext
    :param p: prime
    :param q: prime
    :param e: public exponentiation key
    :return: plaintext
    """
    d = pow(e, -1, (p-1)*(q-1))
    return pow(c, d, p*q)


def miller_rabin(a, n):
    """
    :param a: witness candidate
    :param n: prime candidate
    :return: if a is a Miller-Rabin witness for compositeness of n
    """

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


def pollards_factorization(N, a=2, bound=100):
    """
    :param N: integer to be factored, where N=p*q for primes p & q
    :param a: some convenient integer to expontiate
    :param bound: bound of exponentiation
    :return: a factor of N
    """
    for j in range(1, bound):
        a = pow(a, j, N)
        d = gcd(a-1, N)
        if 1 < d < N:
            return d

    return False  # Couldn't factorize for given a & bound


def difference_of_squares_factorization():
    #TODO
    return


#TODO Quadratic Sieve for finding B-smooth numbers (that have all factors <=B)

def babystep_giantstep(g, h, p):
    """
    :param p: prime
    :return: x, solution of g^x = h (modulo p).
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


