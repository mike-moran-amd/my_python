#!python3
# encoding=utf-8
"""
Prime number generator function written in Python
"""


def generator():
    """
    I wrote this after an interview question about prime numbers and how to prove that there are an infinite number
    of primes separated by only one odd number.
    Using odd multiples and ignoring even numbers speeds up the calculation substantially.
    """
    yield 2  # skipping all other even numbers
    d = {}  # the dictionary of prime multiples
    n = 3  # start at the first odd number
    while True:
        if n in d:  # this number is not prime
            m = d[n]  # but this was
            del d[n]  # we are going to set the next multiple in d
            m2 = m * 2  # m + m is even
            mn = n + m2  # this is the next odd multiple of n
            while mn in d:  # find next empty bucket in d
                mn += m2  # using odd multiples of the original prime m
            d[mn] = m  # store the new multiple of m
        else:  # this is a prime number
            yield n
            # Do we ever clobber another prime?
            # if n*3 in d: print("clobbered", n*3, "which was", d[n*3])
            # 131023: nope, tested up to a million.
            # Is this that one odd prime separator?
            d[n*3] = n  # n is odd, 2*n is even, 3*n is next odd multiple
        n += 2  # next odd number


def nth_prime(limit):
    """
    >>> for ndx in range(10):
    ...    print(f'nth_prime({ndx}) = {nth_prime(ndx)}')
    nth_prime(0) = None
    nth_prime(1) = 2
    nth_prime(2) = 3
    nth_prime(3) = 5
    nth_prime(4) = 7
    nth_prime(5) = 11
    nth_prime(6) = 13
    nth_prime(7) = 17
    nth_prime(8) = 19
    nth_prime(9) = 23

    >>> nth_prime(10)
    29

    >>> nth_prime(100)
    541

    >>> nth_prime(1000)
    7919

    >>> nth_prime(10000)
    104729

    >>> nth_prime(100000)
    1299709

    >>> nth_prime(1000000)  # one millionth prime number, takes about 3 seconds on my laptop
    15485863

    # this takes longer than 3 seconds, so omitted: >>> nth_prime(10000000)  # ten millionth prime number
    179424673

    """
    if limit > 0:
        counter = 1
        for prime in generator():
            counter += 1
            if counter > limit:
                return prime
