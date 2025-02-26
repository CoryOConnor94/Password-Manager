# Password Manager AES

![image](https://github.com/user-attachments/assets/47b44555-7234-4ec7-8805-5d50603c0404)


## Overview
This Password Manager is a secure application built using Python and Tkinter. It allows users to generate, encrypt, store, and retrieve passwords securely using AES-256 encryption. The passwords are stored in a JSON file after encryption, and users can retrieve them using their private key.

## Features
- **Secure Password Generation**: Generates strong 16-character passwords.
- **AES-256 Encryption**: Encrypts passwords using a user-provided private key.
- **Password Storage**: Stores encrypted passwords in a JSON file.
- **Password Retrieval**: Decrypts and retrieves stored passwords when the correct private key is entered.
- **Clipboard Support**: Automatically copies generated and retrieved passwords to the clipboard.
- **User-Friendly GUI**: Built using Tkinter for easy interaction.

## Installation
### Prerequisites
Ensure you have Python installed on your system. Install the required dependencies using pip:

```sh
pip install pycryptodome
```

### Running the Application
Save the script as `password_manager_aes.py` and run:

```sh
python password_manager.py
```

## Usage
### Generating a Password
1. Click the **Generate Password** button.
2. A secure password will be generated and displayed in the password field.
3. The password is automatically copied to the clipboard.

### Saving a Password
1. Enter the website, email/username, and password.
2. Click the **Save** button.
3. You will be prompted to create a private key (used for encryption).
4. Confirm to save the encrypted password.

### Retrieving a Password
1. Enter the website name.
2. Click the **Search** button.
3. You will be prompted to enter your private key (used for decryption).
4. If correct, the decrypted password will be displayed and copied to the clipboard.

## Encryption Details
- **AES-256 in CBC Mode**: Ensures strong encryption security.
- **PBKDF2 Key Derivation**: Strengthens the encryption key using a randomly generated salt.
- **Salt & IV Storage**: Each password entry stores its salt and IV for secure decryption.

## File Storage
Passwords are stored in `secret3.json` in the following format:
```json
{
    "example.com": {
        "email": "user@example.com",
        "password": "<encrypted-password>"
    }
}
```

## Security Considerations
- **Keep your private key safe**: If lost, passwords cannot be decrypted.
- **Use a strong private key**: Enhances encryption security.
- **Avoid sharing the `secret3.json` file**: It contains encrypted data but can be decrypted with the correct private key.

## License
This project is open-source and free to use. Modify and improve it as needed!

