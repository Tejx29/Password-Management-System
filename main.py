import os
from crypto_utils import derive_key, encrypt, decrypt
from fuzzy_strength import password_strength
from chatbot import load_bot
import secrets, string

bot = load_bot()

def get_key(master_password="masterpassword"):
    return derive_key(master_password)

def process_input(user_input: str, username="user1") -> str:
    PASSWORD_FILE = f"data/{username}.dat"
    user_input_strip = user_input.strip()
    user_input_upper = user_input_strip.upper()
    key = get_key("masterpassword")  # Here, ideally derive key from master password

    if user_input_upper.startswith("CREATE PASSWORD"):
        chars = string.ascii_letters + string.digits + string.punctuation
        pw = ''.join(secrets.choice(chars) for _ in range(12))
        token = encrypt(key, pw)
        with open(PASSWORD_FILE, "wb") as f:
            f.write(token)
        return f"Generated Password: {pw}"

    elif user_input_upper.startswith("SHOW PASSWORD"):
        if not os.path.exists(PASSWORD_FILE) or os.path.getsize(PASSWORD_FILE)==0:
            return "No password saved yet."
        with open(PASSWORD_FILE, "rb") as f:
            token = f.read()
        pw = decrypt(key, token)
        return f"Saved Password: {pw}"

    elif user_input_upper.startswith("CHECK PASSWORD"):
        parts = user_input_strip.split(" ", 2)
        if len(parts) < 3:
            return "Please provide a password. Example: CHECK PASSWORD MyPass123!"
        pw = parts[2]
        strength = password_strength(pw)
        return f"Strength: {strength}"

    else:
        return bot.respond(user_input_strip)
