from flask import Flask, render_template, request
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

# Caesar Cipher Encryption Function
def caesar_cipher_encrypt(text, shift):
    result = ""  # Initialize an empty string to store the encrypted result
    for char in text:  # Loop through each character in the input text
        if char.isalpha():  # Check if the character is an alphabet
            # Determine if the character is uppercase or lowercase to set the base
            shift_base = 65 if char.isupper() else 97  
            # Encrypt the character using the Caesar Cipher logic and add to result
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char  # If it's not an alphabet, just add it unchanged
    return result  # Return the encrypted result

# AES Encryption Helper Functions
def pad_message(message):
    # Add spaces to the message until its length is a multiple of 16 (required for AES)
    while len(message) % 16 != 0:
        message += ' '
    return message  # Return the padded message

def aes_encrypt(message, key):
    # Create a new AES cipher object using the provided key in ECB (Electronic Codebook) mode
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    # Encrypt the padded message
    encrypted_message = cipher.encrypt(pad_message(message).encode('utf8'))
    # Encode the encrypted message using base64 and return it as a string
    return base64.b64encode(encrypted_message).decode('utf8')

# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template when the home page is accessed

# Define the route for the encryption process
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Get the message, encryption type, and other parameters from the form data
    message = request.form['message']
    encryption_type = request.form['encryption_type']
    result = ""  # Initialize an empty result string

    # Perform encryption based on the selected type
    if encryption_type == 'caesar':  # If the Caesar Cipher is selected
        shift = int(request.form['shift'])  # Get the shift value from the form
        result = caesar_cipher_encrypt(message, shift)  # Encrypt the message using Caesar Cipher
    elif encryption_type == 'aes':  # If AES is selected
        key = request.form['key']  # Get the AES key from the form
        result = aes_encrypt(message, key)  # Encrypt the message using AES

    # Render the index.html template again, passing the encrypted result and original message
    return render_template('index.html', result=result, message=message, encryption_type=encryption_type)

# Run the application in debug mode when the script is executed
if __name__ == '__main__':
    app.run(debug=True)
