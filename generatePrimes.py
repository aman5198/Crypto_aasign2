from random import randint
import gmpy2 as gmpy

def getRange(min, max):
    rs = gmpy.random_state(hash(gmpy.random_state()))
    return min + gmpy.mpz_random(rs, max - min + 1)

def getRandomInteger(n):
    min = 2**(n-1)
    max = (2**n)-1
    return getRange(min, max)

def largePrimes(n):
    x=getRandomInteger(n)
    s=gmpy.next_prime(x)
    t=gmpy.next_prime(s)
    return s,t

def isPrime(x):
    if gmpy.is_prime(x)==True:
        return 1
    return -1

def generateStrongPrime(s, t, i0, j0, c):
    r=1
    for i in range(c):
        x=2*i*t+1
        if isPrime(x)==1:
            r=x
            break
    p0=2*(gmpy.powmod(s, r-2, r))
    p0=p0*s-1
    for j in range(c):
        p=p0+2*j*r*s
        if isPrime(p)==1:
            return p

    return -1

def getPrivateKey(e, phi):
    d=0
    while e<phi:
        if gmpy.gcd(e, phi)==1:
            if gmpy.invert(e, phi)!=0:
                break
        e=gmpy.add(e,1)
    d=gmpy.invert(e, phi)
    return e, d

def getPrime(n):
    s, t = largePrimes(n)
    i0=randint(100, 10000)
    j0=randint(100, 10000)
    c=1000
    p= generateStrongPrime(s, t, i0, j0, c)

    s, t = largePrimes(n)
    i0=randint(100, 10000)
    j0=randint(100, 10000)
    q= generateStrongPrime(s, t, i0, j0, c)
    n1=p*q
    phi=(p-1)*(q-1)

    s, t = largePrimes(50)
    i0=randint(100, 10000)
    j0=randint(100, 10000)
    e= generateStrongPrime(s, t, i0, j0, c)
    e, d=getPrivateKey(e, phi)

    return p, q, n1, phi, e, d

n=512
p, q, n1, phi, e, d = getPrime(n)
print("All values for first user have been generated using RSA.")
print("p \t",p)
print()
print("q \t",q)
print()
print("n \t",n1)
print()
print("phi \t",phi)
print()
print("e \t",e)
print()
print("d \t",d)
print()