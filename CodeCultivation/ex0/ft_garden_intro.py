#!/usr/bin/env python3

def show(name: str, height: int, age: int):
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days")
    print("=== End of Program ===")


if __name__ == "__main__":
    print("=== Welcome to My Garden ===")
    show("Rose", 25, 30)
