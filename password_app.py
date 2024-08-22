#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import json
import string

LETTERS = string.ascii_letters
DIGITS = string.digits
SPECIAL_CHARS = string.punctuation

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
    password_letters = [choice(LETTERS) for _ in range(10)]
    password_numbers = [choice(DIGITS) for _ in range(3)]
    password_symbols = [choice(SPECIAL_CHARS) for _ in range(3)]

    password_list = password_letters + password_numbers + password_symbols
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
    new_data = {
        website: {
            "email": username,
            "password": password,

        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Blank field", message="Required: Username and Password")
    else:
        try:
            with open("secret.json", "r") as f:
                # Reading old data
                data = json.load(f)

        except FileNotFoundError:
            with open("secret.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)

            with open("secret.json", "w") as f:
                # Saving updated data
                json.dump(data, f, indent=4)
        finally:
            user_website.delete(0, END)
            user_password.delete(0, END)


# ----------------------------FIND PASSWORD---------------------------- #

def find_password():
    """Searches file for existing website data"""
    website = user_website.get()

    try:
        with open("secret.json") as f:
            data = json.load(f)

    except FileNotFoundError:
        messagebox.showerror(title="File Not Found", message="No File Found with that name")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Website Details", message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showerror(title="Website Not Found", message="No details for that website found")


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
