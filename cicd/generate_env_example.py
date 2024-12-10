import ast
import os
from typing import Dict, List, Optional


def find_python_files(base_path: str, ignore: List[str] = None) -> List[str]:
    """
    Recursively find all Python files in the given directory, excluding specified paths.
    :param base_path: Base directory to search.
    :param ignore: List of directories or files to ignore.
    :return: List of Python file paths.
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


def extract_basesettings_fields(file_path: str) -> Dict[str, Optional[str]]:
    """
    Extract fields from Pydantic BaseSettings classes in a Python file.
    Returns a dictionary where keys are field names and values are their default values or None.
    """
    fields = {}
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        # Look for class definitions that inherit from BaseSettings
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseSettings":
                    for body_item in node.body:
                        if isinstance(body_item, ast.AnnAssign) and isinstance(
                            body_item.target, ast.Name
                        ):
                            # Extract field name
                            field_name = body_item.target.id
                            # Extract default value if provided
                            default_value = None
                            if body_item.value:
                                if isinstance(body_item.value, ast.Constant):
                                    default_value = body_item.value.value
                                    if isinstance(
                                        body_item.value.value, (str, int, float, bool)
                                    ):
                                        default_value = str(body_item.value.value)
                            fields[field_name] = default_value
    return fields


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
            fields = extract_basesettings_fields(file)
            env_vars.update(fields)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    with open(output_file, "w") as file:
        for var, default in env_vars.items():
            file.write(f"{var.upper()}={default or ''}\n")
    print(f"Generated {output_file}")


if __name__ == "__main__":
    IGNORE_LIST = [".venv", "__pycache__"]  # Add directories or files to ignore here
    generate_env_example(base_path=".", ignore=IGNORE_LIST)
