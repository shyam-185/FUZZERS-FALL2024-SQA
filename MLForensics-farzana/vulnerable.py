#Testing hook
import os

# Create weak password
DB_PASSWORD = "12345" 

# Insecure function: Shell command injection
def run_command(user_input):
    os.system(f"echo {user_input}")

# Insecure use of eval
def evaluate_expression(expr):
    return eval(expr)

# Unrestricted file read
def read_file(filepath):
    with open(filepath, "r") as file:
        return file.read()
