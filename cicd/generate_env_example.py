import ast
import logging
import os
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(level=logging.INFO)


def generate_centered_string(text: str, total_length: int = 60) -> str:
    dash_length = total_length - len(text)

    if dash_length <= 0:
        return text

    left_dashes = dash_length // 2
    right_dashes = dash_length - left_dashes

    return "-" * left_dashes + text + "-" * right_dashes


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
            env_file = ""  # Default env_file is empty
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
                            # Check for env_prefix and env_file inside model_config
                            if isinstance(body_item.value, ast.Call):
                                for keyword in body_item.value.keywords:
                                    if keyword.arg == "env_prefix" and isinstance(
                                        keyword.value, ast.Constant
                                    ):
                                        env_prefix = keyword.value.value

                                    if keyword.arg == "env_file" and isinstance(
                                        keyword.value, ast.Constant
                                    ):
                                        env_file = keyword.value.value
                                    if env_prefix:
                                        logger.info(
                                            'Environment "%s" found in class %s',
                                            env_prefix,
                                            node.name,
                                        )
                # Extract fields and their default values
                for body_item in node.body:
                    if isinstance(body_item, ast.AnnAssign) and isinstance(
                        body_item.target, ast.Name
                    ):
                        field_name = body_item.target.id
                        default_value = None
                        if isinstance(body_item.value, ast.Constant):  # For Python 3.8+
                            if isinstance(body_item.value.value, (int, float)):
                                default_value = str(body_item.value.value)
                            if isinstance(body_item.value.value, str):
                                default_value = f'"{body_item.value.value}"'
                            if isinstance(body_item.value.value, bool):
                                default_value = str(body_item.value.value).lower()
                        fields[field_name] = default_value

                # Add settings data for this class
                settings_data.append((env_prefix, env_file, fields))

    return settings_data


def generate_env_example(
    base_path: str, output_dir: str = ".", ignore: List[str] = None
) -> None:
    """
    Generate .env.example files based on Pydantic BaseSettings models.
    :param base_path: Base directory to search.
    :param output_dir: Directory to store the generated files.
    :param ignore: List of directories or files to ignore.
    """
    prefix = ".example"
    python_files = find_python_files(base_path, ignore)

    for file in python_files:
        try:
            settings_data = extract_basesettings_fields(file)
            for env_prefix, env_file, fields in settings_data:
                # If env_file is set, use it as the filename
                if env_file:
                    env_file_name = f"{prefix}{env_file.replace('_', '')}"
                else:
                    # If env_file is not set, use the env_prefix as the filename
                    env_file_name = (
                        f"{prefix}.{env_prefix.replace('_', '')}"
                        if env_prefix
                        else f"{prefix}.env"
                    )

                env_file_path = os.path.join(output_dir, env_file_name)

                env_vars: Dict[str, str] = {}

                for field, default in fields.items():
                    # Apply the prefix to the environment variable
                    env_var_name = f"{env_prefix}{field}"
                    env_vars[env_var_name] = default

                # Write the data to the file
                with open(env_file_path, "w", encoding="utf-8") as env_file:
                    header = generate_centered_string(env_file_name.upper())
                    env_file.write(f"# {header}\n")

                    for var, default in env_vars.items():
                        if default is None:
                            default = ""
                        env_file.write(f"{var.upper()}={default}\n")

                    line = generate_centered_string("")
                    env_file.write(f"# {line}\n")
                logger.info("Generated %s", env_file_path)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.info("Error processing file %s: %s", file, e)


if __name__ == "__main__":
    IGNORE_LIST = [".venv", "__pycache__"]  # Add directories or files to ignore here
    generate_env_example(base_path=".", output_dir=".", ignore=IGNORE_LIST)
