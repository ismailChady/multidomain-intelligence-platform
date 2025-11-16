import bcrypt # For password hashing
import os     # For file path checking
import csv    # For CSV reading and writing

# File path for user data
USER_FILE = "Data/users.csv"

# Function to register a new user
def register_user():
    try:
        # Get user input
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")

        # If file doesn't exist, create it with header
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password'])

        # Check if username already exists
        with open(USER_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    print("Username already exists. Try again.")
                    return

        # Hash the password and save user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with open(USER_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password.decode()])
            print("You are registered successfully.")

    except Exception as e:
        print("An error occurred during registration:", e)

# Function to login an existing user
def login_user():
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Check file existence
        if not os.path.exists(USER_FILE):
            print("No users registered yet. Please register first.")
            return False

        # Read and validate login
        with open(USER_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    stored_hashed_password = row['password'].encode()
                    if bcrypt.checkpw(password.encode(), stored_hashed_password):
                        print("Login successful!")
                        return True
                    else:
                        print("Incorrect password. Try again.")
                        return False
            print("Username not found.")
            return False

    except Exception as e:
        print("An error occurred during login:", e)
        return False