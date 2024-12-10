import ast
import os
from typing import Dict, List, Optional, Tuple


def find_python_files(base_path: str, ignore: List[str] = None) -> List[str]:
    """Recursively find all Python files in the given directory, excluding specified paths.

    Args:
        base_path (str): Base directory to search.
        ignore (List[str], optional): List of directories or files to ignore. Defaults to None.

    Returns:
        List[str]: List of Python file paths
    """
    ignore = ignore or []
    python_files = []

    for root, dirs, files in os.walk(base_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                # Filter out ignored files
                if not any(ignored in file_path for ignored in ignore):
                    python_files.append(file_path)
    return python_files


def extract_basesettings_fields(
    file_path: str,
) -> List[Tuple[str, Dict[str, Optional[str]]]]:
    """
    Extract fields and config from Pydantic BaseSettings classes in a Python file.
    Returns a list of tuples, where each tuple contains the `env_prefix` and a dictionary
    of environment variables with their default values.
    """
    settings_data = []
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        # Look for class definitions that inherit from BaseSettings
        if isinstance(node, ast.ClassDef):
            env_prefix = ""  # Default prefix is empty
            fields = {}

            # Check for BaseSettings inheritance
            if any(
                isinstance(base, ast.Name) and base.id == "BaseSettings"
                for base in node.bases
            ):
                # Look for model_config attribute
                for body_item in node.body:
                    if isinstance(body_item, ast.Assign) and isinstance(
                        body_item.targets[0], ast.Name
                    ):
                        if body_item.targets[0].id == "model_config":
                            # Check for env_prefix inside model_config
                            if isinstance(body_item.value, ast.Call):
                                for keyword in body_item.value.keywords:
                                    if keyword.arg == "env_prefix" and isinstance(
                                        keyword.value, ast.Constant
                                    ):
                                        env_prefix = keyword.value.value

                # Extract fields and their default values
                for body_item in node.body:
                    if isinstance(body_item, ast.AnnAssign) and isinstance(
                        body_item.target, ast.Name
                    ):
                        field_name = body_item.target.id
                        default_value = None
                        if isinstance(body_item.value, ast.Constant):  # For Python 3.8+
                            if isinstance(
                                body_item.value.value, (str, int, float, bool)
                            ):
                                default_value = str(body_item.value.value)
                        fields[field_name] = default_value

                # Add settings data for this class
                settings_data.append((env_prefix, fields))

    return settings_data


def generate_env_example(
    base_path: str, output_file: str = ".env.example", ignore: List[str] = None
) -> None:
    """
    Generate a .env.example file based on Pydantic BaseSettings models.
    :param base_path: Base directory to search.
    :param output_file: Name of the output file.
    :param ignore: List of directories or files to ignore.
    """
    python_files = find_python_files(base_path, ignore)
    env_vars: dict[str, str] = {}

    for file in python_files:
        try:
            settings_data = extract_basesettings_fields(file)
            for env_prefix, fields in settings_data:
                for field, default in fields.items():
                    # Apply the prefix to the environment variable
                    env_var_name = f"{env_prefix}{field}"
                    env_vars[env_var_name] = default
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error processing file {file}: {e}")

    with open(output_file, "w", encoding="utf-8") as file:
        for var, default in env_vars.items():
            file.write(f"{var.upper()}={default or ''}\n")
    print(f"Generated {output_file}")


if __name__ == "__main__":
    IGNORE_LIST = [".venv", "__pycache__"]  # Add directories or files to ignore here
    generate_env_example(base_path=".", ignore=IGNORE_LIST)
