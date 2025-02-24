#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import messagebox, simpledialog
from random import choice, shuffle
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import binascii
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
    user_password.delete(0, END)
    # Generate 16 ASCII character password
    password_list = [choice(LETTERS), choice(DIGITS), choice(SPECIAL_CHARS)]    # Ensure one of each in password
    password_list += [choice(ALPHABET) for _ in range(13)]
    shuffle(password_list)  # Shuffle to randomize order
    password = "".join(password_list)
    window.clipboard_clear()  # Clear the clipboard
    print(f"Your password is: {password}\nAlso copied to your clipboard!")
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
    # Call AES encryption function and return encrypted password to be saved
    encrypted_password = aes_encrypt(password, private_key)
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
                                                              f"\nPassword is copied to your clipboard!\n"
                                                              f"\nSelect OK to save")
        if is_ok:
            try:
                with open("secret3.json", "r") as f:
                    # Reading old data
                    data = json.load(f)

            except FileNotFoundError:
                with open("secret3.json", "w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)

                with open("secret3.json", "w") as f:
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
        with open("secret3.json") as f:
            data = json.load(f)

    except FileNotFoundError:
        messagebox.showerror(title="File Not Found", message="No File Found with that name")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            # Prompt user for private key to decrypt password
            private_key = simpledialog.askstring("Decrypt Password", "Enter your private key:")
            # Call AES decrypt function and return decrypted password
            decrypted_password = aes_decrypt(password, private_key)
            window.clipboard_clear()  # Clear the clipboard
            window.clipboard_append(decrypted_password)  # Append decrypted password
            window.update()  # Ensure clipboard update
            messagebox.showinfo(title="Website Details", message=f"Email: {email}\n"
                                                                 f"\nPassword: {decrypted_password}\n"
                                                                 f"\nPassword is copied to your clipboard!")

        else:
            messagebox.showerror(title="Website Not Found", message="No details for that website found")


# ----------------------------DERIVE PRIVATE KEY---------------------------- #

def derive_key(password, salt, iterations=100000):
    """
    Derives a 32-byte (256-bit) cryptographic key from a user-provided password and a randomly generated salt.

    Args:
        password (str): The user-provided password used for key derivation.
        salt (bytes): A 16-byte randomly generated salt to enhance security.

    Returns:
        bytes: The derived 32-byte private key.
    """

    return PBKDF2(password, salt, dkLen=32, count=iterations)


# ----------------------------ENCRYPT PASSWORD---------------------------- #

def aes_encrypt(plain_text, password):
    """
    Encrypts the given plaintext using AES-256 in CBC mode.

    Args:
        plain_text (str): The message to be encrypted.
        password (str): The user-provided password used to derive the encryption key.

    Returns:
        str: The encrypted message as a hexadecimal string, including the salt and IV.
    """

    salt = get_random_bytes(16) # Generate random 16 byte salt
    private_key = derive_key(password, salt) # Derive private key from password and salt

    iv = get_random_bytes(16)  # Generate random 16 byte Initialization vector
    encrypt_cipher = AES.new(private_key, AES.MODE_CBC, iv)   # Create cipher object for encryption

    encrypted_data = encrypt_cipher.encrypt(pad(plain_text.encode(), AES.block_size))   # Encode UTF-8 into bytes for encryption
    return binascii.hexlify(salt + iv + encrypted_data).decode('utf-8') # Store salt, iv and ciphertext together to simplify decryption


# ----------------------------DECRYPT PASSWORD---------------------------- #

def aes_decrypt(encrypted_data, password):
    """
    Decrypts the given ciphertext using AES-256 in CBC mode.

    Args:
        encrypted_data (str): The encrypted message as a hexadecimal string, containing the salt, IV, and ciphertext.
        password (str): The user-provided password used to derive the decryption key.

    Returns:
        str: The decrypted plaintext message.
    """


    cipher_text = binascii.unhexlify(encrypted_data) # Convert hex to bytes for decryption

    salt = cipher_text[:16]     # Extract Salt
    iv = cipher_text[16:32]     # Extract IV
    encrypted_message = cipher_text[32:]   # Extract encrypted message

    private_key = derive_key(password, salt)    # Recompute private key from password and salt
    decrypt_cipher = AES.new(private_key, AES.MODE_CBC, iv)   # Create cipher object for decryption

    decrypted_data = unpad(decrypt_cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_data.decode()


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