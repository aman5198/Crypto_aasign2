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

def getPrivateKey(e, phi, n):
    d=0
    while e<phi:
        if gmpy.gcd(e, phi)==1 and gmpy.gcd(e, n)==1 and gmpy.is_prime(e)==True:
            d=gmpy.invert(e, phi)
            if d!=0 and gmpy.is_prime(d)==True:
                break
        e=gmpy.next_prime(e)
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
    phi=gmpy.mpz((p-1)*(q-1))

    s, t = largePrimes(50)
    i0=randint(100, 10000)
    j0=randint(100, 10000)
    e= generateStrongPrime(s, t, i0, j0, c)
    #e, x = largePrimes(n)
    e, d=getPrivateKey(e, phi,n1)

    return p, q, n1, phi, e, d

def generateAndWriteA(n):
    p, q, n1, phi, e, d = getPrime(n)
    while e<0 or d<0:
        p, q, n1, phi, e, d = getPrime(n)
    print("All values for first user have been generated using RSA.")
    f1 = open("publicA.txt", "w")
    f1.write(str(e))
    f1.write("\n\n")
    f1.write(str(n1))
    f1.write("\n\n")
    f1.write(str(p))
    f1.write("\n\n")
    f1.write(str(q))
    f2 = open("privateA.txt", "w")
    f2.write(str(d))
    f2.write("\n\n")
    f2.write(str(n1))
    f2.write("\n\n")
    f2.write(str(p))
    f2.write("\n\n")
    f2.write(str(q))
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
    f1.close()
    f2.close()
    return p, q, n1, phi, e, d

def generateAndWriteB(n):
    p, q, n1, phi, e, d = getPrime(n)
    while e<0 or d<0:
        p, q, n1, phi, e, d = getPrime(n)
    print("All values for second user have been generated using RSA.")
    f3 = open("publicB.txt", "w")
    f3.write(str(e))
    f3.write("\n\n")
    f3.write(str(n1))
    f3.write("\n\n")
    f3.write(str(p))
    f3.write("\n\n")
    f3.write(str(q))
    f4 = open("privateB.txt", "w")
    f4.write(str(d))
    f4.write("\n\n")
    f4.write(str(n1))
    f4.write("\n\n")
    f4.write(str(p))
    f4.write("\n\n")
    f4.write(str(q))
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
    f3.close()
    f4.close()


n=256
generateAndWriteA(n)
generateAndWriteB(n)