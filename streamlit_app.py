import streamlit as st
import numpy as np
from cipher.affine_cipher import affine_encrypt, affine_decrypt, format_output
from cipher.vignere_cipher import vigenere_encrypt, vigenere_decrypt
from cipher.extendedvignere import extended_vigenere_encrypt, extended_vigenere_decrypt
from cipher.playfair_cipher import playfair_encrypt, playfair_decrypt
from cipher.hill_cipher import encrypt as hill_encrypt, decrypt as hill_decrypt
from cipher.autokey_vignere import encrypt_autokey_vigenere, decrypt_autokey_vigenere

# Konfigurasi halaman
st.set_page_config(page_title="Enkripsi Dekripsi Web Tool", layout="centered")
st.title("🔐 Enkripsi Dekripsi Web Tool")

st.markdown("""
<style>
    div.block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }
    div.stButton > button {
        border-radius: 4px;
        font-weight: 500;
    }
    .stTextArea textarea {
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    div.row-widget.stRadio > div > label {
        margin: 0 10px 0 3px;
    }
</style>
""", unsafe_allow_html=True)

# Pilihan cipher dan operasi
st.subheader("🔧 Pilih Cipher & Operasi")
cipher = st.selectbox("Cipher", ["affine", "vigenere", "extendedvigenere", "playfair", "hill", "autokey"])
operation = st.radio("Operasi", ["encrypt", "decrypt"], horizontal=True)
output_format = st.selectbox("Format output", ["no_space", "group_5"])

# Input parameter kunci
a = b = None
key = ""
matrix = None
error_message = ""
result = ""
content = ""

# Input parameter berdasarkan jenis cipher
if cipher == "affine":
    a = st.number_input("Kunci a (Slope)", value=5, step=1)
    b = st.number_input("Kunci b (Intercept)", value=7, step=1)

if cipher in ["vigenere", "extendedvigenere", "playfair", "autokey"]:
    key = st.text_input("Kunci (Key)", value="RAHASIA")

if cipher == "hill":
    matrix_size = st.selectbox("Ukuran Matrix (NxN)", [2, 3])
    matrix = np.zeros((matrix_size, matrix_size), dtype=int)

    st.write("Masukkan nilai matrix:")
    for i in range(matrix_size):
        cols = st.columns(matrix_size)
        for j in range(matrix_size):
            matrix[i, j] = cols[j].number_input(f"Matrix [{i+1},{j+1}]", value=1, key=f"matrix_{i}_{j}")


# Pilihan jenis input
st.subheader("📤 Input & Output")
input_mode = st.radio("Pilih metode input:", ["Tulis Pesan", "Upload File (.txt)"], horizontal=True)

col1, col2 = st.columns(2)

with col1:
    if input_mode == "Tulis Pesan":
        content = st.text_area("📥 Masukkan pesan (plaintext atau ciphertext)", height=150)
    else:
        uploaded_file = st.file_uploader("📁 Upload file teks (.txt)", type=["txt"])
        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8", errors="ignore")
        else:
            content = ""

# Tombol proses
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
                    try:
                        cipher_bytes = extended_vigenere_encrypt(content.encode(), key.encode())
                        result = cipher_bytes.decode('latin-1')  # Langsung ke karakter latin-1
                    except Exception as e:
                        error_message = f"❌ Error saat enkripsi Extended Vigenère: {e}"
                else:
                    try:
                        cipher_bytes = content.encode('latin-1')  # Ambil dari input karakter
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

# Output di kolom kanan
with col2:
    st.text_area("🔐 Output", result if result else "Output akan muncul di sini setelah diproses.", height=150)

# Tombol download di bawah proses
if result:
    st.download_button("📥 Download Hasil", result, file_name="output.txt")

# Tampilkan error jika ada
if error_message:
    st.error(error_message)
