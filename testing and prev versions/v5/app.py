from flask import Flask, render_template, request
from Crypto.Cipher import AES, DES  # Import DES encryption
from Crypto.PublicKey import RSA  # Import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

app = Flask(__name__)

# Caesar Cipher Encryption Function
def caesar_cipher_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

# AES Encryption Helper Functions
def pad_message(message):
    while len(message) % 16 != 0:
        message += ' '
    return message

def aes_encrypt(message, key):
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad_message(message).encode('utf8'))
    return base64.b64encode(encrypted_message).decode('utf8')

# DES Encryption Function
def des_encrypt(message, key):
    cipher = DES.new(key.encode('utf8'), DES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad_message(message[:8]).encode('utf8'))  # DES works on 8-byte blocks
    return base64.b64encode(encrypted_message).decode('utf8')

# RSA Encryption Function
def rsa_encrypt(message):
    key = RSA.generate(2048)
    public_key = key.publickey()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode('utf8'))
    return base64.b64encode(encrypted_message).decode('utf8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'GET':
        return render_template('encrypt.html')
    
    message = request.form['message']
    encryption_type = request.form['encryption_type']
    result = ""

    if encryption_type == 'caesar':
        shift = int(request.form['shift'])
        result = caesar_cipher_encrypt(message, shift)
    elif encryption_type == 'aes':
        key = request.form['key']
        result = aes_encrypt(message, key)
    elif encryption_type == 'des':
        key = request.form['key'][:8]
        result = des_encrypt(message, key)
    elif encryption_type == 'rsa':
        result = rsa_encrypt(message)
    elif encryption_type == 'unicode':
        result = "Unicode encryption is under development."

    return render_template('encrypt.html', result=result, message=message, encryption_type=encryption_type)


@app.route('/decryption')
def decryption_placeholder():
    return "<h3>Decryption feature coming soon!</h3>"

@app.route('/explanation')
def explanation_placeholder():
    return "<h3>Explanation feature coming soon!</h3>"

if __name__ == '__main__':
    app.run(debug=True)