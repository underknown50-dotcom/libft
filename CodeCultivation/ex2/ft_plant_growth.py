class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self._age: int = age

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self._age} days old")

    def grow(self) -> None:
        self.height += 0.8

    def age(self) -> None:
        self._age += 1


if __name__ == "__main__":
    rose = Plant("Rose", 25.0, 30)

    print("=== Garden Plant Growth ===")
    rose.show()

    old_height = rose.height

    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.age()
        rose.grow()
        rose.show()

    total_height = rose.height - old_height
    print(f"Growth this week: {total_height:.1f}cm")
