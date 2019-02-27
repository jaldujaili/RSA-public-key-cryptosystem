import random

"""The function returns 2 tuples the public and private key"""
def generate_keys():
    # will only hold 2 values for p and q
    keys = []
    # creates random prime numbers within 20-70
    while len(keys)<2:
        num = random.randint(20,70)
        if num in keys:
            num = random.randint(20,70)
        if is_prime(num):
            keys.append(num)
    p,q = keys[0], keys[1]
    print("p: ", p, " q: ",q)
    n = p*q

    # totient of n
    totient = (p - 1) * (q - 1)

    # get an int for e so that e and totient(n) are coprime
    e = random.randrange(1, totient)

    # verify if coprime
    g = gcd(e, totient)
    while g != 1:
        e = random.randrange(1, totient)
        g = gcd(e, totient)

    # generates private key
    d = multi_inverse(e,totient)

    # returns (public key), (private key)
    return ((e,n), (d,n))


"""Euclid's extended algorithm 
    https://stackoverflow.com/questions/11702215/java-inverse-modulo-264/11703184#11703184"""
def multi_inverse(e,totient):
    d,x1,x2,y1,start = 0,0,1,1, totient

    while e>0:
        t1 = start/e
        t2 = start - t1 *e
        start = e
        e = t2
        x = x2-t1*x1
        y = d -t1*y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if start ==1:
        return d+totient

"""This function returns a boolean value if the passed in number is a prime else it will return false"""
def is_prime(num):
    if num == 0 or num == 1:
        return False
    for x in range(2, num):
        if num % x == 0:
            return False
    else:
        return True

"""this function returns the greatest common denominator 
    https://stackoverflow.com/questions/11175131/code-for-greatest-common-divisor-in-python"""
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

def encrypt(private_key, message):
    key, n = private_key
    cipher = []
    # change each letter to unicode and raise to the key and modulo using n
    for letter in message:
        cipher.append((ord(letter) ** key) % n)
    # returns an array of byts
    return cipher

def joiningBytes(cipher):
    return ''.join(cipher)

def decrypt(public_key, cipher):
    key,n = public_key
    regular = []
    # changes byte to char after byte raised to key and modulo n
    for char in cipher:
        regular.append(chr((char ** key) % n))

    # Returns a string
    return ''.join(regular)

if __name__ == '__main__':
    print("Generating public/private keys")
    public, private = generate_keys()
    print("public key: ", public, " private key: ", private)
    msg = raw_input("type a message you want to encrypt:")
    encrypted_msg = encrypt(private, msg)
    print("encrypted msg is: ", joiningBytes(encrypted_msg))
  
    decrypted_msg = decrypt(public, encrypted_msg)
    print("decrypted msg is: ", decrypted_msg)
