import os

from dotenv import load_dotenv, set_key

# Load the example environment variables
load_dotenv(".example.env")

# Define the required environment variables and their default values
required_env_vars = {
    "mqtt_public_host": "default_host",
    "mqtt_username": "default_username",
    "mqtt_password": "default_password",
    "jwt_access_token_secret_key": "default_access_secret",
    "jwt_refresh_token_secret_key": "default_refresh_secret",
}

# Copy .example.env to .env if .env does not exist
if not os.path.exists(".env"):
    with open(".example.env", "r") as example_file:
        with open(".env", "w") as env_file:
            env_file.write(example_file.read())

print("HERE")
# Load the .env file
load_dotenv(".env")

# Fill in missing values
for key, default_value in required_env_vars.items():
    if not os.getenv(key):
        set_key(".env", key.upper(), default_value.upper())
