import string

# Hanya huruf kapital A-Z
ALPHABET = string.ascii_uppercase
ALPHABET_INDEX = {char: idx for idx, char in enumerate(ALPHABET)}

def clean_text(text):
    """ Membersihkan teks dari non-alfabet dan mengubah ke huruf besar. """
    return ''.join(filter(str.isalpha, text.upper()))

def generate_auto_key(plaintext, key):
    """ Menggabungkan kunci dengan plaintext untuk auto-key cipher """
    return key + plaintext[:len(plaintext) - len(key)]

def encrypt_autokey_vigenere(plaintext, key):
    plaintext = clean_text(plaintext)
    key_stream = generate_auto_key(plaintext, clean_text(key))
    ciphertext = ''
    
    for p, k in zip(plaintext, key_stream):
        p_index = ALPHABET_INDEX[p]
        k_index = ALPHABET_INDEX[k]
        c_index = (p_index + k_index) % 26
        ciphertext += ALPHABET[c_index]

    return ciphertext

def decrypt_autokey_vigenere(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key_stream = clean_text(key)
    plaintext = ''
    
    for i in range(len(ciphertext)):
        c_index = ALPHABET_INDEX[ciphertext[i]]
        if i < len(key_stream):
            k_index = ALPHABET_INDEX[key_stream[i]]
        else:
            k_index = ALPHABET_INDEX[plaintext[i - len(key_stream)]]
        p_index = (c_index - k_index + 26) % 26
        plaintext += ALPHABET[p_index]

    return plaintext

def format_five_letters(text):
    """ Format output dalam kelompok 5 huruf """
    return ' '.join(text[i:i+5] for i in range(0, len(text), 5))


# Contoh Penggunaan
if __name__ == "__main__":
    plaintext = input("Masukkan plaintext: ")
    key = input("Masukkan kunci: ")

    cipher = encrypt_autokey_vigenere(plaintext, key)
    print("\nCiphertext (tanpa spasi):", cipher)
    print("Ciphertext (per 5 huruf):", format_five_letters(cipher))

    decrypted = decrypt_autokey_vigenere(cipher, key)
    print("\nDekripsi:", decrypted)
