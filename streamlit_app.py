import streamlit as st
import numpy as np
from cipher.affine_cipher import affine_encrypt, affine_decrypt, format_output
from cipher.vignere_cipher import vigenere_encrypt, vigenere_decrypt
from cipher.extendedvignere import extended_vigenere_encrypt, extended_vigenere_decrypt
from cipher.playfair_cipher import playfair_encrypt, playfair_decrypt
from cipher.hill_cipher import encrypt as hill_encrypt, decrypt as hill_decrypt
from cipher.autokey_vignere import encrypt_autokey_vigenere, decrypt_autokey_vigenere

# UI Judul
st.set_page_config(page_title="Enkripsi Dekripsi Web Tool", layout="centered")
st.title("🔐 Enkripsi Dekripsi Web Tool")

# Input pesan atau upload file
st.subheader("📤 Masukkan Pesan atau Upload File")
message = st.text_area("Tulis pesan plaintext atau ciphertext di sini:", height=150)
uploaded_file = st.file_uploader("Atau upload file teks (.txt)", type=["txt"])
content = message

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8", errors="ignore")

# Pilih cipher
st.subheader("🔧 Pilih Cipher & Operasi")
cipher = st.selectbox("Cipher", [
    "affine", "vigenere", "extendedvigenere", "playfair", "hill", "autokey"
])

operation = st.radio("Operasi", ["encrypt", "decrypt"], horizontal=True)
output_format = st.selectbox("Format output", ["no_space", "group_5"])

# Input kunci sesuai cipher
a = b = None
key = ""
matrix = None
error_message = ""
result = ""

# AFFINE: a & b
if cipher == "affine":
    a = st.number_input("Kunci a (Slope)", value=5, step=1)
    b = st.number_input("Kunci b (Intercept)", value=8, step=1)

# KEY input
if cipher in ["vigenere", "extendedvigenere", "playfair", "autokey"]:
    key = st.text_input("Kunci (Key)", value="RAHASIA")

# MATRIX input
if cipher == "hill":
    matrix_text = st.text_area("Matrix Key (Contoh: 2x2, pisahkan koma dan baris baru)", height=100,
                               value="6,24\n1,13")
    try:
        matrix = np.array([
            list(map(int, row.strip().split(',')))
            for row in matrix_text.strip().splitlines()
        ])
    except Exception as e:
        error_message = f"❌ Error parsing matrix: {e}"

# Proses saat tombol ditekan
if st.button("🚀 Proses"):
    try:
        if not content.strip():
            error_message = "❌ Masukkan pesan atau unggah file terlebih dahulu."
        elif cipher == "affine":
            result = affine_encrypt(content, int(a), int(b)) if operation == "encrypt" else affine_decrypt(content, int(a), int(b))

        elif cipher == "vigenere":
            if not key.isalpha():
                error_message = "❌ Kunci harus berupa huruf."
            else:
                result = vigenere_encrypt(content, key) if operation == "encrypt" else vigenere_decrypt(content, key)

        elif cipher == "extendedvigenere":
            if not key:
                error_message = "❌ Kunci tidak boleh kosong."
            else:
                if operation == "encrypt":
                    result = extended_vigenere_encrypt(content.encode(), key.encode()).hex()
                else:
                    try:
                        cipher_bytes = bytes.fromhex(content.strip())
                        plain_bytes = extended_vigenere_decrypt(cipher_bytes, key.encode())
                        result = plain_bytes.decode('utf-8', errors='replace')
                    except Exception as e:
                        error_message = f"❌ Error saat dekripsi Extended Vigenère: {e}"

        elif cipher == "playfair":
            if not key.isalpha():
                error_message = "❌ Kunci harus berupa huruf."
            else:
                result = playfair_encrypt(content, key) if operation == "encrypt" else playfair_decrypt(content, key)

        elif cipher == "hill":
            if matrix is not None:
                if matrix.shape[0] != matrix.shape[1]:
                    error_message = "❌ Matrix harus berbentuk persegi."
                else:
                    result = hill_encrypt(content, matrix) if operation == "encrypt" else hill_decrypt(content, matrix)
            else:
                error_message = "❌ Matrix tidak valid."

        elif cipher == "autokey":
            if not key.isalpha():
                error_message = "❌ Kunci harus berupa huruf."
            else:
                result = encrypt_autokey_vigenere(content, key) if operation == "encrypt" else decrypt_autokey_vigenere(content, key)

        # Format hasil
        if not error_message:
            result = format_output(result, output_format)

    except Exception as e:
        error_message = f"❌ Terjadi kesalahan saat memproses: {e}"

# Output
if result:
    st.subheader("🧾 Hasil Output")
    st.text_area("Hasil:", result, height=200)
    st.download_button("📥 Download Hasil", result, file_name="output.txt")

# Error
if error_message:
    st.error(error_message)
