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

required_env_app_vars = {
    "APP_ADMIN": "default_admin",
    "APP_PASSWORD": "default_password",
}

required_env_db_vars = {
    "DB_POSTGRES_URL": "postgresql://postgres:example@localhost:5432/postgres",
    "DB_USER": "dev",
    "DB_PASSWORD": "dev_password",
}


def fill_env_file(example_file_path, env_file_path, required_vars):
    # Read the example env file
    with open(example_file_path, "r", encoding="utf-8") as example_file:
        lines = example_file.readlines()

    # Create or overwrite the env file
    with open(env_file_path, "w", encoding="utf-8") as env_file:
        for line in lines:
            # Split the line into key and value
            if "=" in line:
                key, value = line.strip().split("=", 1)
                # If the key is in the required_vars, use the default value if the value is empty
                if key in required_vars and not value:
                    value = required_vars[key]
                env_file.write(f"{key}={value}\n")
            else:
                env_file.write(line)


# Define the paths and corresponding required variables
env_files = {
    ".example.env": (".env", required_env_vars),
    ".example.env.app": (".env.app", required_env_app_vars),
    ".example.env.db": (".env.db", required_env_db_vars),
}

# Fill out the env files
for example_file, (env_file, required_vars) in env_files.items():
    fill_env_file(example_file, env_file, required_vars)
