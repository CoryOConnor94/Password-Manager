import matplotlib.pylab as plt
from random import randint


ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY = 3

def cesar_encrypt(plain_text):
    # Variable to hold the encrypted text
    cipher_text = ''
    # Make case-insensitive
    plain_text = plain_text.upper()

    # Loop through each letter in the plaintext
    for letter in plain_text:
        # Retrieve corresponding index value from alphabet
        letter_index = ALPHABET.find(letter)
        #
        letter_index = (letter_index + KEY) % len(ALPHABET)
        cipher_text = cipher_text + ALPHABET[letter_index]

    return cipher_text


def cesar_decrypt(cipher_text):
    plain_text = ''

    for letter in cipher_text:
        letter_index = ALPHABET.find(letter)

        letter_index = (letter_index - KEY) % len(ALPHABET)
        plain_text = plain_text + ALPHABET[letter_index]

    return plain_text


def crack_ceasar(cipher_text):
    for key in range(len(ALPHABET)):
        plain_text = ''
        for char in cipher_text:
            char_index = ALPHABET.find(char)
            char_index = (char_index - key) % len(ALPHABET)
            plain_text = plain_text + ALPHABET[char_index]
        print(f"With key {key}, plaintext = {plain_text}")


def frequency_analysis(text):
    text = text.upper()
    # Store letter frequency pairs in dictionary
    letter_frequencies = {}

    for char in ALPHABET:
        letter_frequencies[char] = 0

    for char in text:
        if char in ALPHABET:
            letter_frequencies[char] += 1

    return letter_frequencies


def plot_distribution(frequencies):
    plt.bar(frequencies.keys(), frequencies.values())
    plt.show()


def crack_freq_ceasar(cipher_text):
    freq = frequency_analysis(cipher_text)
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    print(f"The possible key value: {ALPHABET.find(freq[0][0]) - ALPHABET.find('E')}")


def vigenere_encrypt(plain_text, key):
    plain_text = plain_text.upper()
    key = key.upper()
    cipher_text = ''
    key_index = 0

    for char in plain_text:
        index = (ALPHABET.find(char) + ALPHABET.find(key[key_index])) % len(ALPHABET)
        cipher_text = cipher_text + ALPHABET[index]
        key_index += 1

        if key_index == len(key):
            key_index = 0

    return cipher_text


def vigenere_decrypt(cipher_text, key):
    cipher_text = cipher_text.upper()
    key = key.upper()
    plain_text = ''
    key_index = 0

    for char in cipher_text:
        index = (ALPHABET.find(char) - ALPHABET.find(key[key_index])) % len(ALPHABET)
        plain_text = plain_text + ALPHABET[index]
        key_index += 1

        if key_index == len(key):
            key_index = 0

    return plain_text


def random_sequence(text):
    random_ints = []

    for _ in range(len(text)):
        random_ints.append(randint(0, len(ALPHABET) - 1))

    return random_ints


def one_time_pad_encrypt(plain_text, key):
    plain_text = plain_text.upper()
    cipher_text = ''

    # Loop through plaintext letters, enumerate returns item + item index
    for index, char in enumerate(plain_text):
        # The value a given letter is shifted
        key_index = key[index]
        # Given letter in plaintext index in Alphabet
        char_index = ALPHABET.find(char)
        # Encrypted message = chars index value + random value index, mod length of alphabet for wrap around
        cipher_text += ALPHABET[(char_index + key_index) % len(ALPHABET)]

    return cipher_text


def one_time_pad_decrypt(cipher_text, key):
    # cipher_text = cipher_text.upper()
    plain_text = ''

    # Loop through each character and return index and value
    for index, char in enumerate(cipher_text):
        # Value given letter will be shifted
        key_index = key[index]
        # Letters index in alphabet
        char_index = ALPHABET.find(char)
        # Decrypted message = char index value - key index value, mod length of alphabet for wrap around
        plain_text += ALPHABET[(char_index - key_index) % len(ALPHABET)]

    return plain_text


# encrypted_message = cesar_encrypt("Dog two")
# decrypted_message = cesar_decrypt(encrypted_message)
# crack_ceasar(encrypted_message)

# text_to_encrypt = input("Enter text here to be encrypted: ")
# private_key = input("Enter private key: ")

# encrypted_message = cesar_encrypt("Dog two")
# decrypted_message = cesar_decrypt(encrypted_message)
# print(decrypted_message)

# crack_ceasar(encrypted_message)

# encrypted_message = vigenere_encrypt(text_to_encrypt, private_key)
# print(encrypted_message)
# decrypted_message = vigenere_decrypt(encrypted_message, private_key)
# print(decrypted_message)


#encrypted_message = cesar_encrypt(text_to_encrypt)
#char_count = frequency_analysis(text_to_encrypt)
#plot_distribution(char_count)
#crack_freq_ceasar(encrypted_message)

message = "This is a secret message to be encrypted using one time pad"
print(f"This is the message to be encrypted: {message}")
sequence = random_sequence(message)
print(f"This is the key of random numbers used to encrypt: {sequence}")
encrypted_message = one_time_pad_encrypt(message, sequence)
print(f"This is the message encrypted: {encrypted_message}")
decrypted_message = one_time_pad_decrypt(encrypted_message, sequence)
print(f"This is the message decrypted: {decrypted_message}")
analysed_encrypted_message = frequency_analysis(encrypted_message)
plot_distribution(analysed_encrypted_message)
