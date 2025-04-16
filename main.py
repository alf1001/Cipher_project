from flask import Flask, render_template, request, send_file
from cipher.affine_cipher import affine_encrypt, affine_decrypt, format_output
from cipher.vignere_cipher import vigenere_encrypt, vigenere_decrypt
from cipher.extendedvignere import extended_vigenere_encrypt, extended_vigenere_decrypt
from cipher.playfair_cipher import playfair_encrypt, playfair_decrypt
from cipher.hill_cipher import encrypt as hill_encrypt, decrypt as hill_decrypt
from cipher.autokey_vignere import encrypt_autokey_vigenere, decrypt_autokey_vigenere
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "encrypted_output.txt")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    output_mode = "no_space"
    error_message = ""

    if request.method == "POST":
        cipher_type = request.form.get("cipher_type")
        operation = request.form.get("operation")
        output_mode = request.form.get("output_format")
        file = request.files.get("file")
        message = request.form.get("message", "")
        key = request.form.get("key", "")
        a = request.form.get("a", type=int)
        b = request.form.get("b", type=int)
        matrix_input = request.form.get("matrix", "")

        content = file.read().decode("utf-8", errors="ignore") if file and file.filename else message

        try:
            if cipher_type == "affine":
                if a is None or b is None:
                    error_message = "Kunci a dan b pada Affine Cipher wajib diisi."
                else:
                    if operation == "encrypt":
                        result = affine_encrypt(content, a, b)
                    else:
                        result = affine_decrypt(content, a, b)

            elif cipher_type == "vigenere":
                if not key.isalpha():
                    error_message = "Terjadi kesalahan dalam kunci Vigenère. Coba gunakan kunci seperti 'RAHASIA'."
                else:
                    if operation == "encrypt":
                        result = vigenere_encrypt(content, key)
                    else:
                        result = vigenere_decrypt(content, key)

            elif cipher_type == "extendedvigenere":
                if not key:
                    error_message = "Kunci Extended Vigenère tidak boleh kosong."
                else:
                    if operation == "encrypt":
                        cipher_bytes = extended_vigenere_encrypt(content.encode(), key.encode())
                        result = cipher_bytes.hex()
                    else:
                        try:
                            cipher_bytes = bytes.fromhex(content.strip())
                            plain_bytes = extended_vigenere_decrypt(cipher_bytes, key.encode())
                            result = plain_bytes.decode('utf-8', errors='replace')
                        except Exception as e:
                            error_message = f"Error saat dekripsi Extended Vigenère: {e}"

            elif cipher_type == "playfair":
                if not key.isalpha():
                    error_message = "Terjadi kesalahan dalam kunci Playfair. Hanya gunakan huruf A-Z tanpa spasi atau angka."
                else:
                    if operation == "encrypt":
                        result = playfair_encrypt(content, key)
                    else:
                        result = playfair_decrypt(content, key)

            elif cipher_type == "hill":
                try:
                    matrix = np.array([
                        list(map(int, row.strip().split(',')))
                        for row in matrix_input.strip().splitlines()
                    ])
                    if matrix.shape[0] != matrix.shape[1]:
                        error_message = "Matrix Hill harus berbentuk persegi (contoh: 2x2 atau 3x3)."
                    else:
                        if operation == "encrypt":
                            result = hill_encrypt(content, matrix)
                        else:
                            result = hill_decrypt(content, matrix)
                except Exception as e:
                    error_message = f"Kesalahan dalam matrix Hill: {e}"

            elif cipher_type == "autokey":
                if not key.isalpha():
                    error_message = "Kunci Autokey Vigenère tidak valid. Gunakan huruf seperti 'RAHASIA'."
                else:
                    if operation == "encrypt":
                        result = encrypt_autokey_vigenere(content, key)
                    else:
                        result = decrypt_autokey_vigenere(content, key)

            if not error_message:
                result = format_output(result, output_mode)
                with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                    f.write(result)

        except Exception as e:
            error_message = f"Terjadi kesalahan: {e}"

    return render_template("index.html", result=result, output_mode=output_mode, error_message=error_message)

@app.route("/download")
def download():
    return send_file(OUTPUT_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
