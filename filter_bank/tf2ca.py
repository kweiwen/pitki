import numpy as np
from math import pi
from scipy import signal

def numrecursion(r, N, c):
    q = np.zeros(N + 1, dtype=complex)

    # Initialize recursion
    q[0] = np.sqrt(-r[0] / c, dtype=complex)
    q[N] = np.conj(c * q[0], dtype=complex)
    q[1] = -r[1] / (2 * c * q[0])
    q[N - 1] = np.conj(c * q[1], dtype=complex)

    # The limit of the for loop depends on the order being odd or even
    for n in range(2, int(np.ceil(N / 2))):
        q[n] = (-r[n] / c - np.sum(q[1:n] * q[n-1:0:-1])) / (2 * q[0])
        q[N-n] = np.conj(c * q[n])

    # Compute middle coefficient separately when order is even
    if N % 2 == 0:
        q[int((N+2) / 2) - 1] = (-r[int((N+2) / 2) - 1] / c - np.sum(q[1:int((N+2) / 2) - 1] * q[int((N+2) / 2) - 2::-1])) / (2 * q[0])

    return q

def powercompnum(b, r, N, c=1):
    """
    Compute numerator of power complementary filter.
    """
    # Check if b is real and c has default value
    if np.isreal(b).all() and c == 1:
        # Try to get a real q with c = 1 and c = -1
        q = numrecursion(r, N, 1)

        if not np.isreal(q).all():
            q = numrecursion(r, N, -1)

        if not np.isreal(q).all():
            print('A real power complementary filter could not be found')
            return q
    else:
        if np.size(c) > 1:
            print('C must be a complex scalar.')
            return None
        if abs(c) - 1 > np.power(np.finfo(float).eps, 2/3):
            print('C must be of magnitude one.')
            return None

        q = numrecursion(r, N, c)

    return q

def auxpoly(b, a):
    revb = np.conj(b[::-1])
    reva = np.conj(a[::-1])

    r = np.subtract(np.convolve(revb, b), np.convolve(a, reva))

    return r

def iirpowcomp(b, a):
    # Find the auxiliary polynomial R(z)
    r = auxpoly(b, a)

    # Compute the numerator of the power complementary transfer function
    q = powercompnum(b, r, len(b) - 1)
    return q, a

def sortnums(b, bp):
    # Sort numerators prior to calling ALLPASSDECOMPOSITION.
    # ALLPASSDECOMPOSITION always requires the first argument to
    # be symmetric. The second argument can be symmetric or antisymmetric.

    # If b is real and antisymmetric, make it the second argument
    if np.max(np.abs(np.add(b, b[::-1]))) < np.finfo(float).eps ** (2 / 3):
        p = bp
        q = b
    else:
        p = b
        q = bp

    return p, q

def allpassdecomposition(p, q, a):
    # If q is real and antisymmetric, make it imaginary
    if np.all(np.isreal(q)):
        if np.max(np.abs(np.add(q, q[::-1]))) < np.finfo(float).eps ** (2 / 3):
            q = q * 1j

    z = np.roots(p - 1j * q)

    # Initialize the allpass functions
    d1 = np.array([1.0])
    d2 = np.array([1.0])

    # Separate the zeros inside the unit circle and the ones outside to form the allpass functions
    for n in range(len(z)):
        if np.abs(z[n]) < 1:
            d2 = np.convolve(d2, [1, -z[n]])
        else:
            d1 = np.convolve(d1, [1, -1 / np.conj(z[n])])

    # Remove roundoff imaginary parts
    d1 = imagprune(d1)
    d2 = imagprune(d2)

    beta = np.sum(d2) * (np.sum(p) + 1j * np.sum(q)) / np.sum(a) / np.sum(np.conj(d2))

    return d1, d2, beta

def imagprune(poly):
    # Function to remove roundoff imaginary parts
    real_part = np.real(poly)
    imag_part = np.imag(poly)
    imag_part[np.abs(imag_part) < np.finfo(float).eps] = 0
    pruned_poly = real_part + imag_part * 1j
    return pruned_poly

def tf2ca(b, a):
    bp, a = iirpowcomp(b, a)
    p, q = sortnums(b, bp)
    d1, d2, beta = allpassdecomposition(p,q,a)
    return d1, d2, beta

def err_diff(d1, d2, a, b):
    
    a0 = a[0]
    
    a = a / a0
    b = b / a0
    
    num = 0.5 * np.convolve(d1[::-1], d2) * beta + 0.5 * np.convolve(d2[::-1], d1) * beta
    den = np.convolve(d1, d2)
    
    return np.abs(np.max([np.max(b-num), np.max(a-den)]))

def neg(d1, d2, beta):
    num = 0.5 * np.convolve(d1[::-1], d2) * beta - 0.5 * np.convolve(d2[::-1], d1) * beta
    den = np.convolve(d1, d2)
    return num, den

def pos(d1, d2, beta):
    num = 0.5 * np.convolve(d1[::-1], d2) * beta + 0.5 * np.convolve(d2[::-1], d1) * beta
    den = np.convolve(d1, d2)
    return num, den

def com(d1, d2, beta):
    num = np.convolve(d1[::-1], d2)
    den = np.convolve(d1, d2)
    return num, den