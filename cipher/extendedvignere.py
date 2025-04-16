import base64

def repeat_key(key: bytes, length: int) -> bytes:
    """Ulangi kunci sampai panjangnya sama dengan data."""
    return (key * (length // len(key) + 1))[:length]

def extended_vigenere_encrypt(data: bytes, key: bytes) -> bytes:
    """Enkripsi data menggunakan Extended Vigenère Cipher."""
    extended_key = repeat_key(key, len(data))
    return bytes((d + k) % 256 for d, k in zip(data, extended_key))

def extended_vigenere_decrypt(data: bytes, key: bytes) -> bytes:
    """Dekripsi data menggunakan Extended Vigenère Cipher."""
    extended_key = repeat_key(key, len(data))
    return bytes((d - k + 256) % 256 for d, k in zip(data, extended_key))

# Contoh penggunaan
if __name__ == "__main__":
    # Data teks
    plaintext = "Halo Dunia!"
    key = "rahasia"

    # Enkripsi
    encrypted = extended_vigenere_encrypt(plaintext.encode(), key.encode())
    print("Encrypted (hex):", encrypted.hex())
    print("Encrypted (base64):", base64.b64encode(encrypted).decode())

    # Dekripsi
    decrypted = extended_vigenere_decrypt(encrypted, key.encode())
    print("Decrypted:", decrypted.decode())
