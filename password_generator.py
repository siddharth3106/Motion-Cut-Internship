import random
import string

def generate_password(length):
    if length < 4:  # Ensure the password is long enough to include all character types
        return "Password length must be at least 4."

    # Character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = "!@#$%^&*()"

    # Ensure at least one character from each category
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_characters)
    ]

    # Fill the rest of the password length with a random mix of all categories
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters
    password += random.choices(all_characters, k=length - 4)

    # Shuffle the password to avoid predictable patterns
    random.shuffle(password)

    return ''.join(password)

# User interaction
def main():
    try:
        length = int(input("Enter the desired password length (minimum 4): "))
        print("Generated Password:", generate_password(length))
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()


