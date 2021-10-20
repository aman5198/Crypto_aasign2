from vigenereEncDec import *
import gmpy2 as gmpy

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

def transform(listOfBlocks, alphabets, blockSize):
    s= ""
    for i in listOfBlocks:
        q=gmpy.mpz(str(i), base=10).digits(26)
        #print(i, "----->", q, "----->", gmpy.mpz(str(q),base=26).digits(10))
        rem=blockSize-len(str(q))
        s=s+" "*rem+str(q)
    return s

def detransform(text, blockSize, alphabets):
    start=0
    end=blockSize
    textBlocks=[]
    for i in range(len(text)):
        x=text[start:end]
        p=gmpy.mpz(x,base=26).digits(10)
        x=x.strip()
        x=x.strip('\n')
        #print(x,"----->",p,"----->",gmpy.mpz(p).digits(26)) 
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

def main():
    key = readKey()

    lengthOfKey=len(key)
    
    message = readMessage()
    #print(key, message)
    viegenereMessage = encryption() 

    data = open("blockSize.txt",'r').readlines()
    blockSize = int(data[0])
    
    alphabets=26

    key=key+"Z"

    messageBlocks, keyBlocks = createBlocks(viegenereMessage, key, blockSize, alphabets)
    # print(messageBlocks)
    # print(keyBlocks)

    n1, d1, p1, q1 = getKeys("PrivateA.txt")

    n2, e2, p2, q2 = getKeys("PublicB.txt")
    
    messageEncrypted = encrypt(messageBlocks, n2, e2)
    keyEncrypted = encrypt(keyBlocks, n2, e2)

    #Digitally signing the message and key has been done. Now we encrypt the message using receiver's public key

    messageSigned = encrypt(messageEncrypted, n1, d1)
    keySigned = encrypt(keyEncrypted, n1, d1)

    # print(messageEncrypted)
    # print(keyEncrypted)

    #Message has been encrypted using receiver's public key. Now we have to transform it to send.

    for i in messageSigned:
        if blockSize<(gmpy.num_digits(gmpy.mpz(i),alphabets)):
            blockSize = (gmpy.num_digits(gmpy.mpz(i),alphabets))
    #print(blockSize)

    messageTransformed = transform(messageSigned, alphabets, blockSize)
    keyTransformed = transform(keySigned, alphabets, blockSize)

    print("The Message to be sent is:\n",messageTransformed)
    print("The Key to be sent is:\n",keyTransformed)

    f = open("messageToSend.txt", "w")
    f.write(messageTransformed)
    f.write("\n\n")
    f.write(keyTransformed)
    f.write("\n\n")
    f.write(str(blockSize))
    
    #Digitally signing the message and key has been done. Now we encrypt the message using receiver's public key
    
    blockSize=5
    for i in keyEncrypted:
        if blockSize<(gmpy.num_digits(gmpy.mpz(i),alphabets)):
            blockSize = (gmpy.num_digits(gmpy.mpz(i),alphabets))
    print(blockSize)
    KeyToVerify = transform(keyEncrypted, alphabets, blockSize).strip()
    
    f.write("\n\n")
    f.write(str(blockSize))
    f.write("\n\n")
    f.write(KeyToVerify)
    f.close()

    print("\nMessage has been digitally signed and encrypted using RSA cryptosystem.\n")


main()