def caesar_cipher_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

if __name__ == "__main__":
    message = input("Enter a message to encrypt using Caesar Cipher: ")
    shift = int(input("Enter the shift value: "))
    encrypted_message = caesar_cipher_encrypt(message, shift)
    print(f"Encrypted message: {encrypted_message}")
