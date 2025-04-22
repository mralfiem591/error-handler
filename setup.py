import os
import json
from cryptography.fernet import Fernet

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths for key and config files
KEY_PATH = os.path.join(BASE_DIR, "key.key")
CONFIG_PATH = os.path.join(BASE_DIR, "errorconfig.json")

# Step 1: Generate and save the encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key saved to '{KEY_PATH}'.")

# Step 2: Encrypt the GitHub token
def encrypt_token(token):
    with open(KEY_PATH, "rb") as key_file:
        key = key_file.read()
    cipher = Fernet(key)
    encrypted_token = cipher.encrypt(token.encode())
    return encrypted_token.decode()

# Step 3: Create the errorconfig.json file
def create_config(encrypted_token, repo, app_name):
    config = {
        "app_name": app_name,
        "app_version": "1.0.0",
        "error_screen_text": "Oops! Something went wrong. Please report this issue.",
        "enable_standalone": True,
        "github_repo": repo,
        "github_token": encrypted_token,
        "ui_colors": {
            "title": "bold red",
            "text": "yellow",
            "input": "cyan"
        }
    }
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(config, config_file, indent=4)
    print(f"Configuration file saved to '{CONFIG_PATH}'.")

# Main setup process
def main():
    print("Setting up the error reporter...")

    # Generate the encryption key
    generate_key()

    # Ask for user input
    github_token = input("Enter your GitHub token: ").strip()
    repo = input("Enter the GitHub repository (format: username/repo): ").strip()
    app_name = input("Enter the app name: ").strip()

    # Encrypt the GitHub token
    encrypted_token = encrypt_token(github_token)

    # Create the configuration file
    create_config(encrypted_token, repo, app_name)

    print("Setup complete!")

if __name__ == "__main__":
    main()