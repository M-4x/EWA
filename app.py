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
        message += " "
    return message

def aes_encrypt(message, key):
    cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad_message(message).encode("utf8"))
    return base64.b64encode(encrypted_message).decode("utf8")

# DES Encryption Function
def des_encrypt(message, key):
    cipher = DES.new(key.encode("utf8"), DES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad_message(message[:8]).encode("utf8"))
    return base64.b64encode(encrypted_message).decode("utf8")

# RSA Encryption Function
def rsa_encrypt(message, public_key_data):
    public_key = RSA.import_key(public_key_data)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode("utf8"))
    return base64.b64encode(encrypted_message).decode("utf8")

# Caesar Cipher Decryption Function
def caesar_cipher_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            result += char
    return result

# AES Decryption Function
def aes_decrypt(encrypted_message, key):
    cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
    decoded_message = base64.b64decode(encrypted_message)
    decrypted_message = cipher.decrypt(decoded_message).decode("utf8").rstrip()
    return decrypted_message

# DES Decryption Function
def des_decrypt(encrypted_message, key):
    cipher = DES.new(key.encode("utf8"), DES.MODE_ECB)
    decoded_message = base64.b64decode(encrypted_message)
    decrypted_message = cipher.decrypt(decoded_message).decode("utf8").rstrip()
    return decrypted_message

# RSA Decryption Function
def rsa_decrypt(encrypted_message, private_key_data):
    private_key = RSA.import_key(private_key_data)
    cipher = PKCS1_OAEP.new(private_key)
    try:
        decoded_message = base64.b64decode(encrypted_message)
        decrypted_message = cipher.decrypt(decoded_message).decode("utf8")
        return decrypted_message
    except (ValueError, TypeError) as e:
        return f"Decryption error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "GET":
        return render_template("encrypt.html")

    message = request.form["message"]
    encryption_type = request.form["encryption_type"]
    result = ""

    if encryption_type == "caesar":
        shift = int(request.form["shift"])
        result = caesar_cipher_encrypt(message, shift)
    elif encryption_type == "aes":
        key = request.form["key"]
        result = aes_encrypt(message, key)
    elif encryption_type == "des":
        key = request.form["key"][:8]
        result = des_encrypt(message, key)
    elif encryption_type == "rsa":
        public_key_data = request.form["public_key"]
        result = rsa_encrypt(message, public_key_data)
    elif encryption_type == "unicode":
        return render_template("encrypt.html")

    return render_template("encrypt.html", result=result, message=message, encryption_type=encryption_type)

@app.route("/decryption", methods=["GET", "POST"])
def decryption():
    if request.method == "GET":
        return render_template("decryption.html")

    encrypted_message = request.form["encrypted_message"]
    decryption_type = request.form["decryption_type"]
    result = ""

    if decryption_type == "caesar":
        shift = int(request.form["shift"])
        result = caesar_cipher_decrypt(encrypted_message, shift)
    elif decryption_type == "aes":
        key = request.form["key"]
        result = aes_decrypt(encrypted_message, key)
    elif decryption_type == "des":
        key = request.form["key"][:8]
        result = des_decrypt(encrypted_message, key)
    elif decryption_type == "rsa":
        private_key_data = request.form["private_key"]
        result = rsa_decrypt(encrypted_message, private_key_data)
    elif decryption_type == "unicode":
        return render_template("decryption.html")

    return render_template("decryption.html", result=result, encrypted_message=encrypted_message, decryption_type=decryption_type)

@app.route("/explanation")
def explanation_menu():
    return render_template("explanation.html")

@app.route("/explanation/<level>")
def explanation_level(level):
    return render_template("explanation_level.html", level=level)


# Caesar Cipher Explanations
@app.route("/explanation/layman/caesar")
def caesar_layman():
    return render_template("caesar_layman.html")


@app.route("/explanation/comprehensive/caesar")
def caesar_comprehensive():
    return render_template("caesar_comprehensive.html")


@app.route("/explanation/implementation/caesar")
def caesar_implementation():
    return render_template("caesar_implementation.html")


# AES Explanations
@app.route("/explanation/layman/aes")
def aes_layman():
    return render_template("aes_layman.html")


@app.route("/explanation/comprehensive/aes")
def aes_comprehensive():
    return render_template("aes_comprehensive.html")


@app.route("/explanation/implementation/aes")
def aes_implementation():
    return render_template("aes_implementation.html")


# RSA Explanations
@app.route("/explanation/layman/rsa")
def rsa_layman():
    return render_template("rsa_layman.html")


@app.route("/explanation/comprehensive/rsa")
def rsa_comprehensive():
    return render_template("rsa_comprehensive.html")


@app.route("/explanation/implementation/rsa")
def rsa_implementation():
    return render_template("rsa_implementation.html")


# DES Explanations
@app.route("/explanation/layman/des")
def des_layman():
    return render_template("des_layman.html")


@app.route("/explanation/comprehensive/des")
def des_comprehensive():
    return render_template("des_comprehensive.html")


@app.route("/explanation/implementation/des")
def des_implementation():
    return render_template("des_implementation.html")


# Unicode Placeholder Explanations
@app.route("/explanation/layman/unicode")
def unicode_layman():
    return render_template("unicode_layman.html")


@app.route("/explanation/comprehensive/unicode")
def unicode_comprehensive():
    return render_template("unicode_comprehensive.html")


@app.route("/explanation/implementation/unicode")
def unicode_implementation():
    return render_template("unicode_implementation.html")


if __name__ == "__main__":
    app.run(debug=True)
