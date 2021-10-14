from vigenereEncDec import *
import gmpy2 as gmpy

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

def detransform(text, blockSize, alphabets):
    start=0
    end=blockSize
    textBlocks=[]
    for i in range(len(text)):
        x=text[start:end]
        #print(start,"   ",end,"   ",x)
        x=x.strip(' ')
        p=gmpy.mpz(x,base=26).digits(10)
        textBlocks.append(p)
        i=end
        start=end
        end=end+blockSize
        if i>=len(text):
            break
    return textBlocks


def check(first, second):
    for i in range(len(first)):
        if gmpy.mpz(first[i])!=gmpy.mpz(second[i]):
            print(gmpy.mpz(first[i]))
            print(gmpy.mpz(second[i]))
            print(i)
            return False
    return True

def filtering(key):
    k=""
    for i in range(len(key)):
        if key[i]=='Z':
            break
        k=k+key[i]
    return k

def vigenereDecryption(listOfBlocks):
    data = open("blockSize.txt",'r').readlines()
    blockSize = int(data[0])
    alphabets=26
    string=""

    for i in listOfBlocks:
        text=""
        arr=[]
        for j in range(blockSize):
            x=int((i%alphabets))
            arr.append(x)
            i=gmpy.mpz(i/alphabets)
            
        arr=arr[::-1]
        for j in arr:
            text=text+chr(j+65)
        string=string+text

    return string

def main():
    data = open("messageToSend.txt",'r').readlines()
    message = (data[0])
    key = (data[2])
    # print(message)
    # print(key)
    blockSize = int(data[4])
    alphabets=26
    message=message.strip('\n')
    key=key.strip('\n')
    
    messageToDecrypt = detransform(message, blockSize, alphabets)
    keyToDecrypt = detransform(key, blockSize, alphabets)

    # print(messageToDecrypt)
    # print(keyToDecrypt)

    n1, e1, p1, q1 = getKeys("PublicA.txt")

    n2, d2, p2, q2 = getKeys("PrivateB.txt")

    messageDecrypted = encrypt(messageToDecrypt, n2, d2)
    keyDecrypted = encrypt(keyToDecrypt, n2, d2)

    message1 = encrypt(messageDecrypted, n1, e1)
    key1 = encrypt(keyDecrypted, n1, e1)

    # print(message1)
    # print(key1)

    encryptedVigenere=vigenereDecryption(message1)
    encryptedKey=vigenereDecryption(key1)

    realKey = filtering(encryptedKey)
    print("\nKey used by sender was: ",realKey)
    print("\nVigenere encrypted message sent by sender was: ",encryptedVigenere)

    #Decyption back using vigenere key is left now.

    finalDecryptedMessage = decryptionWithParam(encryptedVigenere, realKey)

    print("\nTHE FINAL DECRYPTED MESSAGE IS: ")
    print(finalDecryptedMessage)
    print()


main()