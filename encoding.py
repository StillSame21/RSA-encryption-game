"""
encoding.py
-----------
Converts text strings to integers and back
Convention: standard ASCII, uppercase only
Block size: 4 letters = 8-digit integer  
"""

BLOCK_SIZE = 4

def clean_message(text):
    """
    Uppercase the text
    remove every character that is not a letter. Spaces are removed here (as required by
    remove spaces before decode
    """
    result =""
    for ch in text.upper():
        if ch.isalpha():
            result += ch
    return result

def letter_to_code(ch):
    """
    convert char into ASCII code (built in function)s
    """
    return ord(ch)     

def code_to_letter(code):
    """
    convert ASCII code into char (built in function)
    """
    return chr(code)         

def block_to_number(block):
    """
    conver 4 letter block into 8 digit ASCII code
    """
    code_str = "".join(str(letter_to_code(ch)) for ch in block)
    return int(code_str)


def number_to_block(number, size=BLOCK_SIZE):
    """
    Convert 8 digit ASCII code into strings of letter 
    """
    digits = str(number).zfill(size * 2)   # ensure 8 digits
    letters = []
    for i in range(0, len(digits), 2):
        code = int(digits[i:i+2])
        letters.append(code_to_letter(code))
    return "".join(letters)


def text_to_blocks(text, size=BLOCK_SIZE):
    """
    clean plaintext and add padding as needed
    """
    cleaned = clean_message(text)
    # pad to multiple of size
    remainder = len(cleaned) % size
    if remainder != 0:
        cleaned += 'X' * (size - remainder)
    
    blocks = []
    for i in range(0, len(cleaned), size):
        block = cleaned[i:i+size]
        blocks.append(block)
    return blocks


def encrypt_message(text, e, n, encrypt_fn):
    """
    calling function to process plaintext to ciphertext
    """
    blocks   = text_to_blocks(text)
    numbers  = [block_to_number(b) for b in blocks]
    ciphers  = [encrypt_fn(m, e, n) for m in numbers]
    return ciphers


def decrypt_message(cipher_list, d, n, decrypt_fn):
    """
    calling function to process ciphertext to plaintext
    """
    numbers = [decrypt_fn(c, d, n) for c in cipher_list]
    blocks  = [number_to_block(m)  for m in numbers]
    text    = "".join(blocks)
    return text.rstrip('X')     # remove padding
