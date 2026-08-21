import bcrypt

def generate_password_hash(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

if __name__ == "__main__":
    password = input("Enter a password to hash: ")
    hashed_password = generate_password_hash(password)
    print(f"\nBcrypt hash:\n{hashed_password}")
