import unicodedata


def main():
    LONG = 9223372036854775807
    NEG_LONG = -9223372036854775806
    count = 0
    skip_increment = 100  # Increment to avoid skipped symbols

    print("Encrypt/Decrypt?")
    encdec = input()

    def is_renderable(charpos):
        """
        Check if a character is renderable and valid for output.
        """
        try:
            char = chr(charpos)
            # Check if the character is displayable
            if unicodedata.category(char) in ["Cs", "Cn"]:
                return False
            return True
        except ValueError:
            return False

    if encdec.lower() in ["encrypt", "e"]:
        print("Type what you want to encrypt")
        input_text = input()
        print("How many characters shift")
        shift = int(input())
        print("How many multipliers")
        multi = int(input())
        print("Type your multipliers")
        array = [int(input()) for _ in range(multi)]

        if shift > 93:
            shift = 93
        elif shift < -32:
            shift = -32

        encrypted_text = ""

        for char in input_text:
            charpos = ord(char)
            shift *= array[count]
            charpos += shift

            # Normalize charpos within the Unicode range
            charpos = ((charpos - 33) % (1114112 - 33 + 1)) + 33

            # Skip over problematic symbols
            while not is_renderable(charpos):
                charpos = ((charpos + skip_increment - 33) % (1114112 - 33 + 1)) + 33

            asciic = chr(charpos)
            encrypted_text += asciic

            if shift > 0:
                shift += 1
            elif shift < 0:
                shift -= 1

            count += 1
            if count >= multi - 1:
                count = 0

            if shift > 1114112:
                shift = 33
            elif shift < -1114112:
                shift = -33

        print("\nEncrypted Text:")
        print(encrypted_text)

    elif encdec.lower() in ["decrypt", "d"]:
        print("Type what you want to decrypt")
        input_text = input()
        print("How many characters shift")
        shift = int(input())
        shift *= -1
        print("How many multipliers")
        multi = int(input())
        print("Type your multipliers")
        array = [int(input()) for _ in range(multi)]

        decrypted_text = ""

        for char in input_text:
            charpos = ord(char)
            shift *= array[count]
            charpos += shift

            # Normalize charpos within the Unicode range
            charpos = ((charpos - 33) % (1114112 - 33 + 1)) + 33

            # Skip over problematic symbols
            while not is_renderable(charpos):
                charpos = ((charpos + skip_increment - 33) % (1114112 - 33 + 1)) + 33

            asciic = chr(charpos)
            decrypted_text += asciic

            if shift < 0:
                shift -= 1
            else:
                shift += 1

            count += 1
            if count >= multi - 1:
                count = 0

            if shift > 1114112:
                shift = 33
            elif shift < -1114112:
                shift = -33

        print("\nDecrypted Text:")
        print(decrypted_text)

    else:
        print("ERROR")


if __name__ == "__main__":
    main()
