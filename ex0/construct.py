import sys
import os
import site


def is_inside_venv() -> bool:
    return sys.prefix != sys.base_prefix


def get_python_executable() -> str:
    return sys.executable


def get_venv_name() -> str:
    if is_inside_venv():
        return os.path.basename(sys.prefix)
    return "None detected"


def get_venv_prefix() -> str:
    return sys.prefix


def get_site_packages_path() -> str:
    paths = site.getsitepackages()
    return paths[0]


def print_outside_message(python_path: str) -> None:
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {python_path}")
    print("Virtual Environment: None detected")
    print()
    print(
        "WARNING: You're in the global environment! "
        "The machines can see everything you install."
    )
    print()
    print("To enter the construct, run:")
    print("  python -m venv matrix_env")
    print("  source matrix_env/bin/activate  # On Unix")
    print("  matrix_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")


def print_inside_message(
    python_path: str,
    venv_name: str,
    venv_prefix: str,
    site_packages: str,
) -> None:
    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {python_path}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_prefix}")
    print()
    print(
        "SUCCESS: You're in an isolated environment! Safe to install "
        "packages without affecting the global system."
    )
    print()
    print(f"Package installation path: {site_packages}")


def main() -> None:
    python_path = get_python_executable()

    if is_inside_venv():
        venv_name = get_venv_name()
        venv_prefix = get_venv_prefix()
        site_packages = get_site_packages_path()
        print_inside_message(
            python_path,
            venv_name,
            venv_prefix,
            site_packages,
        )
    else:
        print_outside_message(python_path)


if __name__ == "__main__":
    main()
