from alchemy import create_air


if __name__ == "__main__":
    print("== Alembic 5 ==")
    print("Accessing the alchemy module using ’from alchemy import ...’")
    result = create_air()
    print(f"Testing create_air: {result}")
