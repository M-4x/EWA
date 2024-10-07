from Crypto.Cipher import AES
import base64

def pad_message(message):
    while len(message) % 16 != 0:
        message += ' '
    return message

def aes_encrypt(message, key):
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad_message(message).encode('utf8'))
    return base64.b64encode(encrypted_message).decode('utf8')

if __name__ == "__main__":
    message = input("Enter a message to encrypt using AES: ")
    key = "thisisakey123456"
    encrypted_message = aes_encrypt(message, key)
    print(f"Encrypted message: {encrypted_message}")
