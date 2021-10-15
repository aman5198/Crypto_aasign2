from vigenereEncDec import *
import gmpy2 as gmpy
from generatePrimes import *

def createBlocks(message, key, blockSize, alphabets):
    i=0
    messageBlocks = []
    keyBlocks = []
    while i<(len(message)):
        j = blockSize-1
        innerSum = 0
        while j>=0:
            currentChar = message[i]
            innerSum = innerSum+int(ord(currentChar)-65)*(alphabets**j)
            i = i+1
            j = j-1
            if i>=(len(message)):
                break
        messageBlocks.append(innerSum)

    i=0
    while i<(len(key)):
        j = blockSize-1
        innerSum = 0
        while j>=0:
            currentChar = key[i]
            innerSum = innerSum+int(ord(currentChar)-65)*(alphabets**j)
            i = i+1
            j = j-1
            if i>=(len(key)):
                break
        keyBlocks.append(innerSum)

    return messageBlocks, keyBlocks

def encrypt(listOfBlocks, n, a):
    transformedBlock=[]
    for i in listOfBlocks:
        x=gmpy.powmod(gmpy.mpz(i), a, n)
        transformedBlock.append(x)
    return transformedBlock

def getKeys(path):
    data = open(path,'r').readlines()
    k = gmpy.mpz(data[0])
    n1 = gmpy.mpz(data[2])
    p = gmpy.mpz(data[4])
    q = gmpy.mpz(data[6])
    return n1, k, p, q

def check(first, second):
    for i in range(len(first)):
        if gmpy.mpz(first[i])!=gmpy.mpz(second[i]):
            # print(gmpy.mpz(first[i]))
            # print(gmpy.mpz(second[i]))
            # print(i)
            return False
    return True

def checkValidityOfKeys():
    key = readKey()
    message = readMessage()

    viegenereMessage = encryption() 

    data = open("blockSize.txt",'r').readlines()
    blockSize = int(data[0])
    
    alphabets=26

    key=key+"Z"
    messageBlocks, keyBlocks = createBlocks(viegenereMessage, key, blockSize, alphabets)
    
    # print(messageBlocks)
    # print(keyBlocks)

    n1, d1, p1, q1 = getKeys("PrivateA.txt")
    n1, e1, p1, q1 = getKeys("PublicA.txt")

    n2, d2, p2, q2 = getKeys("PrivateB.txt")
    n2, e2, p2, q2 = getKeys("PublicB.txt")

    messageSigned = encrypt(messageBlocks, n1, d1)
    keySigned = encrypt(keyBlocks, n1, d1)

    #Digitally signing the message and key has been done. Now we encrypt the message using receiver's public key

    messageEncrypted = encrypt(messageSigned, n2, e2)
    keyEncrypted = encrypt(keySigned, n2, e2)

    #Message has been encrypted using receiver's public key. Now we have to transform it back into letters.

    messageDecrypted = encrypt(messageEncrypted, n2, d2)
    keyDecrypted = encrypt(keyEncrypted, n2, d2)

    message1 = encrypt(messageDecrypted, n1, e1)
    key1 = encrypt(keyDecrypted, n1, e1)

    res1 = (check(message1,messageBlocks))
    res2 = (check(key1,keyBlocks))

    # print(message1)
    # print(key1)

    return (res1 and res2)

n=256
generateAndWriteA(n)
generateAndWriteB(n)
while checkValidityOfKeys()==False:
    print("GeneratingKeys...")
    generateAndWriteA(n)
    generateAndWriteB(n)
print("----------------KEYS GENERATED----------------")