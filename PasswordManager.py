import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from random import choice

symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4',
           ,'5' ',6' ,'7' ,'8' ,'9', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
            '{', '}', '|', ':', '"', '<', '>', '?'] # this is a symbols for create password

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = self._derive_key()
        self.fernet = Fernet(self.key)
        self.passwords = {}

    def _derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'salt_',  # In a real application, use a random salt and store it
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
        return key

    def add_password(self, website, username, password):
        encrypted_password = self.fernet.encrypt(password.encode())
        self.passwords[website] = (username, encrypted_password)
        print(f"Password for {website} added successfully.")

    def get_password(self, website):
        if website in self.passwords:
            username, encrypted_password = self.passwords[website]
            decrypted_password = self.fernet.decrypt(encrypted_password).decode()
            return username, decrypted_password
        else:
            return None

    def list_websites(self):
        return list(self.passwords.keys())

# Example usage
def main():
    master_password = input("Enter your master password: ")
    pm = PasswordManager(master_password)

    while True:
        print("\n1. Add a password")
        print("2. Get a password")
        print("3. List all websites")
        print('4. Create a password')
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            pm.add_password(website, username, password)
        elif choice == '2':
            website = input("Enter website: ")
            result = pm.get_password(website)
            if result:
                username, password = result
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("Website not found.")
        elif choice == '3':
            websites = pm.list_websites()
            print("Stored websites:")
            for site in websites:
                print(site)
        elif choise == '4':
            lenofpassword = int(input('What is len of password?: '))
            password = ''
            for i in range(lenofpassword):
                password = password + random.choice(symbols)
            print(f'this is your password: {password}')
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Test the Password Manager
print("Testing Password Manager...")
test_pm = PasswordManager("test_master_password")
test_pm.add_password("example.com", "user@example.com", "password123")
test_pm.add_password("github.com", "githubuser", "securepass")

print("\nStored websites:", test_pm.list_websites())

print("\nRetrieving password for example.com:")
username, password = test_pm.get_password("example.com")
print(f"Username: {username}")
print(f"Password: {password}")

print("\nRetrieving password for github.com:")
username, password = test_pm.get_password("github.com")
print(f"Username: {username}")
print(f"Password: {password}")
