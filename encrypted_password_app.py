#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import messagebox, simpledialog
from random import choice, shuffle
import json
import string

LETTERS = string.ascii_letters
DIGITS = string.digits
SPECIAL_CHARS = string.punctuation
ALPHABET = string.ascii_letters + string.digits + string.punctuation + " "

WINDOW_BG = "#020203"
FIELD_COLORS = "#272b2b"
FIELD_FONT_COLOR = "#07d6fa"
LABEL_COLOR = "#10cf02"
FONT = ("Courier", 12, "normal")

# ----------------------------PASSWORD GENERATOR---------------------------- #


def password_generator():
    """Generates secure 16 character password"""
    global LETTERS, DIGITS, SPECIAL_CHARS
    user_password.delete(0, END)
    # Generate 16 ASCII character password
    password_list = [choice(ALPHABET) for _ in range(16)]
    # password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    print(f"Your password is: {password}")
    user_password.insert(0, password)
    user_password.clipboard_append(password)


# ----------------------------SAVE PASSWORD---------------------------- #

def save():
    """Saves data to file"""
    website = user_website.get()
    username = user_name.get()
    password = user_password.get()
    # Prompt user to create private key used to Encrypt/Decrypt password
    private_key = simpledialog.askstring("Encrypt Password", "Create your private key:")
    # Call vigenere encryption function and return encrypted password to be saved
    encrypted_password = vigenere_encrypt(password, private_key)
    new_data = {
        website: {
            "email": username,
            "password": encrypted_password,

        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Blank field", message="Required: Username and Password")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Website: {website}\n"
                                                              f"\nEmail/UserName: {username}\n"
                                                              f"\nPassword: {encrypted_password}\n"
                                                              f"\nSelect OK to save")
        if is_ok:
            try:
                with open("secret2.json", "r") as f:
                    # Reading old data
                    data = json.load(f)

            except FileNotFoundError:
                with open("secret2.json", "w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)

                with open("secret2.json", "w") as f:
                    # Saving updated data
                    json.dump(data, f, indent=4)
            finally:
                user_website.delete(0, END)
                user_password.delete(0, END)

        else:
            user_website.delete(0, END)
            user_name.delete(0, END)
            user_password.delete(0, END)


# ----------------------------FIND PASSWORD---------------------------- #

def find_password():
    """Searches file for existing website data"""
    website = user_website.get()

    try:
        with open("secret2.json") as f:
            data = json.load(f)

    except FileNotFoundError:
        messagebox.showerror(title="File Not Found", message="No File Found with that name")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            # Prompt user for private key to decrypt password
            private_key = simpledialog.askstring("Decrypt Password", "Enter your private key:")
            # Call vigenere decrypt function and return decrypted password
            decrypted_password = vigenere_decrypt(password, private_key)
            messagebox.showinfo(title="Website Details", message=f"Email: {email}\n Password: {decrypted_password}")
        else:
            messagebox.showerror(title="Website Not Found", message="No details for that website found")


# ----------------------------ENCRYPT PASSWORD---------------------------- #

def vigenere_encrypt(plain_text, key):
    """
    Encrypts the given plain_text using the Vigenère cipher algorithm.

    Args:
        plain_text (str): The message to be encrypted.
        key (str): The encryption key, a sequence of characters to be used cyclically.

    Returns:
        str: The encrypted message (cipher_text).
    """
    # Initialize an empty string to store the encrypted message.
    cipher_text = ''
    # Index to track the position in the key.
    key_index = 0

    # Loop through each character in the plain text.
    for char in plain_text:
        # Find the index of the current character and corresponding key character in the ALPHABET.
        char_index = (ALPHABET.find(char) + ALPHABET.find(key[key_index])) % len(ALPHABET)
        # Append the encrypted character to the cipher_text.
        cipher_text += ALPHABET[char_index]
        # Move to the next character in the key.
        key_index += 1

        # If the end of the key is reached, reset the key index to start again.
        if key_index == len(key):
            key_index = 0

    return cipher_text


# ----------------------------DECRYPT PASSWORD---------------------------- #
def vigenere_decrypt(cipher_text, key):
    """
    Decrypts the given cipher_text using the Vigenère cipher algorithm.

    Args:
        cipher_text (str): The encrypted message to be decrypted.
        key (str): The decryption key, a sequence of characters to be used cyclically.

    Returns:
        str: The decrypted message (plain_text).
    """
    # Initialize an empty string to store the decrypted message.
    plain_text = ''
    # Index to track the position in the key.
    key_index = 0

    # Loop through each character in the cipher text.
    for char in cipher_text:
        # Find the index of the current character and corresponding key character in the ALPHABET.
        char_index = (ALPHABET.find(char) - ALPHABET.find(key[key_index])) % len(ALPHABET)
        # Append the decrypted character to the plain_text.
        plain_text += ALPHABET[char_index]
        # Move to the next character in the key.
        key_index += 1

        # If the end of the key is reached, reset the key index to start again.
        if key_index == len(key):
            key_index = 0

    return plain_text


# ----------------------------UI SETUP---------------------------- #
# Window setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WINDOW_BG)

# Canvas setup
canvas = Canvas(width=200, height=200, bg=WINDOW_BG, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Label Setup
website_label = Label(text="Website:", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
website_label.grid(column=0, row=1, padx=3, pady=3)

username_label = Label(text="Email/Username:", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
username_label.grid(column=0, row=2, padx=3, pady=3)

password_label = Label(text="Password:", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
password_label.grid(column=0, row=3, padx=3, pady=3)


# Entry Setup
user_website = Entry(width=35, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
user_website.grid(column=1, row=1, columnspan=2, padx=3, pady=3)
user_website.focus()

user_name = Entry(width=35, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
user_name.grid(column=1, row=2, columnspan=2, padx=3, pady=3)

user_password = Entry(width=35, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
user_password.grid(column=1, row=3, columnspan=2, padx=3, pady=3)

# Button setup
generate_button = Button(text="Generate Password", width=35, command=password_generator, font=FONT)
generate_button.grid(column=1, row=5, columnspan=2)

add_button = Button(text="Save", width=17, font=FONT, command=save)
add_button.grid(column=3, row=3)

search_button = Button(text="Search", width=17, font=FONT, command=find_password)
search_button.grid(column=3, row=1)


window.mainloop()