# Vigenere and RSA combination.

1. python3 generatePublicAndPrivateKeys.py: Generates Public and Private Keys for users A and B.
2. python3 encryption.py: First Encrypts the message with vigenere cipher and the on message and key it applies the digital signature using sender's private key and encryption using receiver's public key.
3. python3 decryption.py: Does Decryption using receiver's private key and verifies digital signature using sender's public key. At the end it decrypts the message using vigenere cipher key.

This code uses gmpy2 i.e the GNU Multi precision library to generate large prime number for generation of strong primes. RSA uses strong primes p and q.