import alchemy

if __name__ == "__main__":
    print("== Alembic 4 ==")
    print("Using 'import alchemy' to access the module")

    print(f"Testing create_air: {alchemy.create_air()}")

    print("\nNow show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth:")

    try:
        alchemy.create_earth()  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"  {e}")
