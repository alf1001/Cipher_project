import re

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def clean_text(text):
    return re.sub(r'[^A-Za-z]', '', text).upper()

def vigenere_encrypt(plaintext, key):
    plaintext = clean_text(plaintext)
    key = clean_text(key)
    if not key:
        return ''
    cipher = []
    key_len = len(key)
    for i, char in enumerate(plaintext):
        p = ALPHABET.index(char)
        k = ALPHABET.index(key[i % key_len])
        c = (p + k) % 26
        cipher.append(ALPHABET[c])
    return ''.join(cipher)

def vigenere_decrypt(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key = clean_text(key)
    if not key:
        return ''
    plain = []
    key_len = len(key)
    for i, char in enumerate(ciphertext):
        c = ALPHABET.index(char)
        k = ALPHABET.index(key[i % key_len])
        p = (c - k + 26) % 26
        plain.append(ALPHABET[p])
    return ''.join(plain)

def group_five(text):
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])
