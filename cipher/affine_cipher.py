import string

ALPHABET = string.ascii_uppercase
M = 26

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def affine_encrypt(text, a, b):
    result = ""
    for char in clean_text(text):
        x = ALPHABET.index(char)
        encrypted_char = ALPHABET[(a * x + b) % M]
        result += encrypted_char
    return result

def affine_decrypt(cipher, a, b):
    a_inv = mod_inverse(a, M)
    if a_inv is None:
        return "Invalid key: 'a' must be coprime with 26"
    result = ""
    for char in clean_text(cipher):
        y = ALPHABET.index(char)
        decrypted_char = ALPHABET[(a_inv * (y - b)) % M]
        result += decrypted_char
    return result

def format_output(text, mode):
    if mode == "no_space":
        return text
    elif mode == "group_5":
        return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])
    return text
