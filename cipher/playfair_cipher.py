import string

def generate_key_square(key):
    key = ''.join(filter(str.isalpha, key.upper()))
    key = key.replace('J', 'I')  # Gabungkan J ke I
    seen = set()
    result = ''
    for char in key + string.ascii_uppercase:
        if char not in seen and char != 'J':
            seen.add(char)
            result += char
    return [list(result[i:i+5]) for i in range(0, 25, 5)]

def preprocess_text(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    return text.replace('J', 'I')  # Gabungkan J ke I

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None  # Antisipasi karakter tidak ditemukan

def prepare_digraphs(text):
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            digraphs.append(a + 'X')
            i += 1
        else:
            digraphs.append(a + b)
            i += 2
    if len(digraphs[-1]) == 1:
        digraphs[-1] += 'X'
    return digraphs

def playfair_encrypt(plain_text, key):
    matrix = generate_key_square(key)
    text = preprocess_text(plain_text)
    digraphs = prepare_digraphs(text)
    cipher = ''

    for digraph in digraphs:
        a, b = digraph
        pos1 = find_position(matrix, a)
        pos2 = find_position(matrix, b)

        if not pos1 or not pos2:
            raise ValueError(f"Karakter '{a}' atau '{b}' tidak ditemukan dalam matriks Playfair.")

        row1, col1 = pos1
        row2, col2 = pos2

        if row1 == row2:
            cipher += matrix[row1][(col1 + 1) % 5]
            cipher += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher += matrix[(row1 + 1) % 5][col1]
            cipher += matrix[(row2 + 1) % 5][col2]
        else:
            cipher += matrix[row1][col2]
            cipher += matrix[row2][col1]

    return cipher

def playfair_decrypt(cipher_text, key):
    matrix = generate_key_square(key)
    text = preprocess_text(cipher_text)
    digraphs = [text[i:i+2] for i in range(0, len(text), 2)]
    plain = ''

    for digraph in digraphs:
        a, b = digraph
        pos1 = find_position(matrix, a)
        pos2 = find_position(matrix, b)

        if not pos1 or not pos2:
            raise ValueError(f"Karakter '{a}' atau '{b}' tidak ditemukan dalam matriks Playfair.")

        row1, col1 = pos1
        row2, col2 = pos2

        if row1 == row2:
            plain += matrix[row1][(col1 - 1) % 5]
            plain += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plain += matrix[(row1 - 1) % 5][col1]
            plain += matrix[(row2 - 1) % 5][col2]
        else:
            plain += matrix[row1][col2]
            plain += matrix[row2][col1]

    return plain
