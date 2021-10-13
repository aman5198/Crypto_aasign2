def readKey():
    data=open("KwithM.txt",'r').readlines()
    key=data[0].rstrip().upper()
    keyCheck=list([val for val in key if val.isalpha()])
    key="".join(keyCheck)  
    return key

def readMessage():
    data=open("KwithM.txt",'r').readlines()
    message=data[1].upper()
    messageCheck=list([val for val in message if val.isalpha()])
    message="".join(messageCheck)
    return message

def readCipher():
    data=open("Vencrypted.txt",'r').readlines()
    cipher=data[0].upper()
    cipherCheck=list([val for val in cipher if val.isalpha()])
    cipher="".join(cipherCheck)
    return cipher


def setKey(message,key):
    newKey=list(key)
    if len(message) == len(key):
        return
    else:
        for i in range(len(message) - len(key)):
            newKey.append(key[i%len(key)])
    
    return ("".join(newKey))


def encryption():
    key=readKey()
    message=readMessage()
    key=setKey(message,key)
    encrypted = []

    for i in range(len(message)):
        x=((ord(key[i])+ord(message[i]))%26 ) + ord('A')
        encrypted.append(chr(x))
    encrypted="".join(encrypted)

    file=open("Vencrypted.txt" , 'w')
    file.write(encrypted)

def decryption():
    key=readKey()
    cipher=readCipher()
    key=setKey(cipher,key)
    decrypted = []

    for i in range(len(cipher)):
        x=((ord(cipher[i])-ord(key[i]))%26 )+ ord('A')
        decrypted.append(chr(x))
    decrypted="".join(decrypted)
    file=open("Vdecrypted.txt", 'w')
    file.write(decrypted)








encryption() 
decryption()









