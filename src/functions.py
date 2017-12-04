#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains many math and cipher functions
"""

import sys
import string
import random
import itertools
from math import sqrt, floor
from random import randint, getrandbits

def rotl(n, rotations=1, w=32):
    """ binary rotation (left)

        Args:
            n -- int -- number to rotate,
            rotations -- int -- number of rotations

        return n rotated
    """
    return ((n << rotations) | (n >> w - rotations))

def bytearray_xor(b1, b2):
    """ xor 2 bytearray

        Args:
            b1 -- bytearray
            b2 -- bytearray

        return a bytearray
    """
    result = bytearray()
    for x, y in zip(b1, b2):
        result.append(x ^ y)
    return result

def find_group_generators(n):
    """ Find the generators of a cyclic group of order n

        Start by finding all coprimes of n.
        Then, for each i in range[1, n], test if it generates all coprimes of n

        Args:
            n -- int -- cyclic group's order

        return the list of generators
    """

    coprimes = []

    # find coprimes of n
    for k in range(1, n):
        if are_coprime(k, n):
            coprimes.append(k)


    generators = []

    # find generators
    for i in range(1, n):
        temp = []
        for j in range(1, n):
            temp.append(i**j % n)

        if len(set(temp)) == len(coprimes):
            generators.append(i)

    return generators

def gcd(a, b):
    """ Calculate the gcd of a and b recursively, using euclidean_algorithm

		Args:
			a -- int
			b -- int

		return the gcd of a and b
	"""
    return euclidean_algorithm(a, b)


def lcm(a, b):
    """ Search the lowest positive integer than can be devide by a and b

		Args:
			a -- int
			b -- int

		return the lcm of a and b
	"""
    return (a*b) // gcd(a, b)


def bezout(a, b):
    """ Calculate the Bézout's identity of 'a' and 'b'
	"""
    result, x, y = euclidean_algorithm(a, b, extended=True)

	# if x and y are reversed, fix it
    if (a*x + b*y) != result:
        x, y = y, x

	# print Bezout identity
	# print("BEZOUT(%d, %d) : %d * %d + %d * %d = %d " % (a, b, x, a, y, b, result))

    return result, x, y


def euclidean_algorithm(a, b, x=0, prev_x=1, y=1, prev_y=0, extended=False, step=1):
    """ Run the euclidean algorithm to calculate the gcd of a and b
		If extended is True, calculate x and y for the Bézout's identity

		Step is usefull to know which factor is negative => if even, it's 'y' else it's 'x'

        a -- int
        b -- int
        x -- int -- usefull for Bezout identity
        prev_x -- int -- previous value of x
        y -- int -- usefull for Bezout identity
        prev_y -- int -- previous value of y
        extended -- boolean -- if true, keep track of x and y for Bezout identity
        step -- int -- algorithm's current step

        return the gcd, x and y
	"""
	# 'a' has to be greater than 'b'
    if b > a:
        a, b = b, a

	# calculate the remainder of a/b
    remainder = a % b

	# if remainder is 0, stop here : gcd found
    if remainder == 0:
        if not extended:
            return b
        else:
			# use the step parameter to calculate which factor is negative
            x *= (-1)**step
            y *= (-1)**(step+1)
            return b, x, y

	# we continue
    if extended:
		# if extended, update x and y and increment the step
        step += 1
        quotient = a // b
        prev_x, prev_y, x, y = x, y, quotient*x + prev_x, quotient*y + prev_y
        return euclidean_algorithm(b, remainder, x, prev_x, y, prev_y, extended=True, step=step)
    else:
        return euclidean_algorithm(b, remainder, step=step)

def are_coprime(a, b):
    """ Two integers are coprime if their gcd is 1

        Args:
            a -- int
            b -- int

        return true if they are coprime
	"""
    return gcd(a, b) is 1


def is_prime(n):
    """ Check if n is prime

        Args:
            n -- int

        return true if it's prime
	"""
    if n == 1:
        return False

    for i in range(2, int(sqrt(n))):
        if n % i == 0:
            return False
    return True


def random_prime(start = 0, end = 500):
    """ Return a random prime between start and end

        Args:
            start -- int -- lowest value for the prime number
            end -- int -- biggest value for the prime number

        return a prime number randomly picked
    """
    primes = sieve_of_eratosthenes(end)
    i = 0
    while i < len(primes) and primes[i] < start:
        i += 1
    primes = primes[i:]

    if len(primes) == 0:
        return 2

    return primes[randint(0, len(primes)-1)]

def prime_decomposition(n):
    """ Find the prime numbers pn (recursively) so that
		n = p1^a1 * p2^a2 * ... * pn^an

        Args:
            n -- int -- the number of decompose
            primes -- list -- the primes factors
	"""
    for i in itertools.chain([2], itertools.count(3, 2)):
        if n <= 1:
            break
        while n % i == 0:
            n //= i
            yield i

def exponentiation_by_squaring_recursive(n, exp):
    """ Fast way to do exponentiation, recursively

        Args:
            n -- int
            exp -- int -- the exponent

        return n**exp
    """
	# stop when exp is 1
    if exp == 1:
        return n

    if exp % 2 == 1:
        return n * exponentiation_by_squaring(n**2, (exp-1)//2)
    else:
        return exponentiation_by_squaring(n**2, exp//2)

def exponentiation_by_squaring(n, exp):
    """ Fast way to do exponentiation

        Args:
            n -- int
            exp -- int -- the exponent

        return n**exp
    """
    y = 1
    while exp > 1:
        if exp % 2 == 1:
            y *= n
            n *= n
            exp = (exp-1) // 2
        else:
            n **= 2
            exp //= 2

    return n * y


def inverse(n, mod):
    """ Calculate the inverse of 'n' modulo 'mod' using bezout identity

        Args:
            n -- int
            mod -- int

        return the inverse modulos mod of n
	"""
    _, inv, _ = bezout(n, mod)
    return inv


def chinese_remainder_theorem(values, modulos):
    """ Solve the following system of congruences
			x = a1 (mod m1)
			x = a2 (mod m2)
			...
			x = an (mod mn)

		values -- list -- contains a1, a2, ..., an
		modules -- list -- contains m1, m2, ..., mn

		return x
	"""

    M = 1
    for m in modulos:
        M *= m
    x = 0

	# for each equation in the system
    for i, modulo in enumerate(modulos):
        Mi = M // modulo
        x += values[i] * Mi * inverse(Mi, modulo)

    return x


def phi(n):
    """ Euler's totient function. Count the number of integers that
		are relative primes with n in range [1, n-1]

        Args:
            n -- int

        return the number of relative primes
	"""

	# if n is prime, all numbers < n are prime with it
    if is_prime(n):
        return n-1

	# get the integers that are part of the prime decomposition of n
    primes = list(set(prime_decomposition(n)))

    result = n
    for prime in primes:
        result *= (1 - (1 /prime))
    return int(result)


def sieve_of_eratosthenes(n):
    """ Search and return the primes lower or equals to 'n'

        Args:
            n -- int

        return list of primes
	"""
    primes = []
    numbers = range(2, n+1)

	# continu while there are numbers
    while len(numbers):
		# the first is a prime
        primes.append(numbers[0])

		# remove all the multiple of the first number
        next_numbers = []
        for i in range(1, len(numbers)):
            if numbers[i] % numbers[0] > 0:
                next_numbers.append(numbers[i])
        numbers = next_numbers

    return primes


def fermat_primality_test(n, k=1):
    """ Probabilistic test to determine if n is prime

        Args:
            n -- int -- the number to test for primality
            k -- int -- the number of tests

        return False if not prime, or True if it seems to be prime
	"""
    if n < 2:
        return False

    if n > 3:
        for _ in range(k):
            random = randint(2, n-2)
            if exponentiation_by_squaring(random, n-1) % n != 1:
                return False

    return True


def miller_rabin_primality_test(n, k=2):
    """ Probabilistic test to determine if n is prime

        Args:
            n -- int -- the number to test for primality
            k -- int -- the number of tests

        return False if not prime, or True if it seems to be prime
	"""
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r = 0
    s = n - 1
    while s & 1 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def monoalphabetic_substitution_cipher(message, plaintext_alphabet, ciphertext_alphabet):
    """ monoalphabetic substitution cipher implementation for uppercase alpha letters

        Args:
            messsage -- string -- the message to cipher
            plaintext_alphabet -- string -- message's alphabet
            ciphertext_alphabet -- string -- alphabet to cipher the message

        return the ciphertext
    """
    message = message.upper()
    plaintext_alphabet_dic = {k: v for v, k in enumerate(plaintext_alphabet)}
	# return the encrypted message
    return ''.join([ciphertext_alphabet[plaintext_alphabet_dic[c]] for c in message])


def affine_block_encryption(plaintext, a, b):
    """ Encryption function of the affine block cypher
		blocks of size 2

		Given Mi and M(i+1) = Mj
		x = i * 26 + j
		(a * x + b) mod 26^2 = Ci * 26 + Cj

        Args:
            plaintext -- string -- the text to cipher
            a -- int -- linear coefficient
            b -- int -- ordinate at origin

        return ciphertext
	"""
	# make sure the plaintext has an even length (because blocks of 2)
    if len(plaintext) % 2 == 1:
        sys.exit("It's required that the plaintext has an even length")

    plaintext = plaintext.upper()
    alphabet = string.ascii_uppercase
    alphabet_dic = {k: v for v, k in enumerate(string.ascii_uppercase)}
	# return the ciphertext
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
		# calculate the x in (ax + b)
        x = (alphabet_dic[plaintext[i]]*26) + alphabet_dic[plaintext[i+1]]
        E = (a * x + b) % 676
        Ci = alphabet[E // 26]
        Cj = alphabet[E % 26]
        ciphertext += Ci + Cj
    return ciphertext


def affine_block_decryption(ciphertext, a, b):
    """ Decryption function of the affine block cypher
		blocks of size 2

		Given Ci and C(i+1) = Cj
		y = i * 26 + j
		D = a^-1 * (y - b) mod 26^2
		Mi = D // 26
		Mj = D % 26

        Args:
            ciphertext -- string -- the text to decipher
            a -- int -- linear coefficient
            b -- int -- ordinate at origin

        return plaintext
	"""
	# make sure the message has an even length (because blocks of 2)
    if len(ciphertext) % 2 == 1:
        sys.exit("It's required that the encrypted message has an even length")

    ciphertext = ciphertext.upper()
    alphabet = string.ascii_uppercase
    alphabet_dic = {k: v for v, k in enumerate(string.ascii_uppercase)}
	# return the encrypted message
    message = ""
    for i in range(0, len(ciphertext), 2):
        y = (alphabet_dic[ciphertext[i]]*26) + alphabet_dic[ciphertext[i+1]]
        D = inverse(a, 676) * (y - b)
		# mod 26^2
        D -= floor(D/676) * 676
        Mi = alphabet[D // 26]
        Mj = alphabet[D % 26]

        message += Mi + Mj

    return message

def generate_prime_candidate(length=1025):
    """
        Generate an integer that has a chance to be prime

        Args:
            length -- int -- the size in bits of the number to generate

        return an integer
    """
    # generate random bits
    p = list(str(bin(getrandbits(length)))[2:])
    # check the size
    if len(p) < length:
        p = ['0']*(length-len(p)) + p
    if len(p) > length:
        p = p[:length]
    # Set the MSB to 1
    p[0] = '1'
    # Set the LSB to 1 (else, has 0 chance to be prime)
    p[len(p) - 1] = '1'
    # transform the list of string to int
    return int(''.join(p), 2)


def generate_prime_number(length=1025):
    """
        Generate a prime number

        Args:
            length -- int -- the size of the prime number to generate, in bits

        return a number which is very probably a prime number
    """
    p = 4
    # continue while the primality test fail
    while not miller_rabin_primality_test(p, 128):
        p = generate_prime_candidate(length)

    return p


def generate_safe_prime_number(length=1025):
    """
        Generate a prime safe number (where p = 2q + 1, with q prime)

        Args:
            length -- int -- the size of the prime number to generate, in bits

        return a number which is very probably a prime safe prime number
    """
    p = 4
    # continue while the primality test fail
    while not miller_rabin_primality_test(p, 128):
        # generate q
        q = generate_prime_candidate(length-1)
        # calculate p = 2*q + 1
        p = (q << 1) | 1
    return p


def find_safe_prime_generator(p, q):
    """
        Find a generator a cyclic group G where the order is a safe prime:
        => the prime factors are 2 and q

        Args:
            p -- int -- the order of the cyclic group
            q -- int -- a prime number, where p = 2q - 1

        return a generator of p
    """
    a = randint(0, p-1)
    while pow(a, (p-1)//2, p) == 1 or pow(a, (p-1)//q, p) == 1:
        a = randint(0, p-1)
    return a
