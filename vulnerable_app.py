"""
vulnerable_app.py
-----------------
A deliberately insecure Python login & file management app.
Created for CodeAlpha Task 3 — Secure Coding Review.
DO NOT use this code in production.
"""

import os
import pickle
import sqlite3
import hashlib
import subprocess
import yaml

# ------------------------------------------------------------------ #
#  VULNERABILITY 1: Hardcoded credentials (SC050 / SC051)
# ------------------------------------------------------------------ #
SECRET_KEY = "supersecretkey123"
DB_PASSWORD = "admin1234"
API_KEY = "sk-abc123def456ghi789"

# ------------------------------------------------------------------ #
#  VULNERABILITY 2: MD5 password hashing (SC013)
# ------------------------------------------------------------------ #
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# ------------------------------------------------------------------ #
#  VULNERABILITY 3: SQL Injection via string concatenation (SC057)
# ------------------------------------------------------------------ #
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Dangerous: user input directly injected into query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

# ------------------------------------------------------------------ #
#  VULNERABILITY 4: Command Injection via os.system (SC010)
# ------------------------------------------------------------------ #
def ping_host(hostname):
    # Dangerous: user-controlled input passed to shell
    os.system("ping -c 1 " + hostname)

# ------------------------------------------------------------------ #
#  VULNERABILITY 5: Insecure deserialization with pickle (SC006)
# ------------------------------------------------------------------ #
def load_session(session_file):
    with open(session_file, "rb") as f:
        # Dangerous: pickle.loads can execute arbitrary code
        session = pickle.loads(f.read())
    return session

# ------------------------------------------------------------------ #
#  VULNERABILITY 6: eval() on user input (SC001)
# ------------------------------------------------------------------ #
def calculate(expression):
    # Dangerous: executes arbitrary Python code
    result = eval(expression)
    return result

# ------------------------------------------------------------------ #
#  VULNERABILITY 7: subprocess with shell=True (SC030)
# ------------------------------------------------------------------ #
def list_files(directory):
    output = subprocess.check_output("ls " + directory, shell=True)
    return output

# ------------------------------------------------------------------ #
#  VULNERABILITY 8: yaml.load without Loader (SC031)
# ------------------------------------------------------------------ #
def load_config(config_file):
    with open(config_file, "r") as f:
        # Dangerous: yaml.load without Loader can execute code
        config = yaml.load(f)
    return config

# ------------------------------------------------------------------ #
#  VULNERABILITY 9: Debug mode enabled (SC055)
# ------------------------------------------------------------------ #
DEBUG = True

# ------------------------------------------------------------------ #
#  VULNERABILITY 10: Plain HTTP URL (SC056)
# ------------------------------------------------------------------ #
API_ENDPOINT = "http://api.externalservice.com/data"

# ------------------------------------------------------------------ #
#  VULNERABILITY 11: assert used for security check (SC040)
# ------------------------------------------------------------------ #
def delete_user(username, is_admin):
    assert is_admin, "Only admins can delete users"
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()

# ------------------------------------------------------------------ #
#  VULNERABILITY 12: Insecure random for token generation (SC015)
# ------------------------------------------------------------------ #
import random
def generate_token():
    # Dangerous: random is not cryptographically secure
    return str(random.randint(100000, 999999))


if __name__ == "__main__":
    if DEBUG:
        print("[DEBUG] App starting...")
    print("Login system running.")
    print(f"Token: {generate_token()}")
