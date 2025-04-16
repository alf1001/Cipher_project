import numpy as np
import string

ALPHABET = string.ascii_uppercase
MOD = 26

def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def text_to_numbers(text):
    return [ALPHABET.index(char) for char in text]

def numbers_to_text(numbers):
    return ''.join(ALPHABET[num % MOD] for num in numbers)

def chunk_text(text, size):
    padding = (size - len(text) % size) % size
    text += 'X' * padding
    return [text[i:i+size] for i in range(0, len(text), size)]

def mod_inverse(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))
    det %= modulus
    det_inv = pow(det, -1, modulus)
    matrix_mod_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_mod_inv.astype(int)

def encrypt(text, key_matrix):
    text = clean_text(text)
    size = key_matrix.shape[0]
    chunks = chunk_text(text, size)
    ciphertext = ''
    for chunk in chunks:
        P = np.array(text_to_numbers(chunk)).reshape((size, 1))
        C = key_matrix.dot(P) % MOD
        ciphertext += numbers_to_text(C.flatten())
    return ciphertext

def decrypt(text, key_matrix):
    text = clean_text(text)
    size = key_matrix.shape[0]
    key_inv = mod_inverse(key_matrix, MOD)
    chunks = chunk_text(text, size)
    plaintext = ''
    for chunk in chunks:
        C = np.array(text_to_numbers(chunk)).reshape((size, 1))
        P = key_inv.dot(C) % MOD
        plaintext += numbers_to_text(P.flatten())
    return plaintext
