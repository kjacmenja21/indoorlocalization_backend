# Define the required environment variables and their default values
required_env_vars = {
    "MQTT_PUBLIC_HOST": "default_host",
    "MQTT_HOST": "default_host",
    "MQTT_PORT": "1883",
    "MQTT_USERNAME": "default_username",
    "MQTT_PASSWORD": "default_password",
    "JWT_ACCESS_TOKEN_SECRET_KEY": "default_access_secret",
    "JWT_REFRESH_TOKEN_SECRET_KEY": "default_refresh_secret",
}

# Read the .example.env file
with open(".example.env", "r", encoding="utf-8") as example_file:
    lines = example_file.readlines()

# Create or overwrite the .env file
with open(".env", "w", encoding="utf-8") as env_file:
    for line in lines:
        # Split the line into key and value
        if "=" in line:
            key, value = line.strip().split("=", 1)
            # If the key is in the required_env_vars, use the default value if the value is empty
            if key in required_env_vars and not value:
                value = required_env_vars[key]
            env_file.write(f"{key}={value}\n")
        else:
            env_file.write(line)
