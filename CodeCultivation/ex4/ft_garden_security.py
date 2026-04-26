class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> float:
        return self._height

    def set_height(self, height: float) -> None:
        if height >= 0:
            self._height = height
        else:
            print(f"{self._name}: Error, height can't be negative")

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> None:
        if age >= 0:
            self._age = age
        else:
            print(f"{self._name}: Error, age can't be negative")

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._age} days old")


if __name__ == "__main__":
    print("=== Garden Security System ===")

    plant = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    plant.show()

    plant.set_height(25.0)
    print("Height updated: 25cm")

    plant.set_age(30)
    print("Age updated: 30 days")

    plant.set_height(-5.0)
    print("Height update rejected")

    plant.set_age(-10)
    print("Age update rejected")

    print("Current state: ", end="")
    plant.show()
