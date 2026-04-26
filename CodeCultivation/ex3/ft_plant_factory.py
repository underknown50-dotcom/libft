class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age: int = age

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.age} days old")


if __name__ == "__main__":
    print("=== Plant Factory Output ===")

    plant1: Plant = Plant("Rose", 25.0, 30)
    print("Created: ", end="")
    plant1.show()

    plant2: Plant = Plant("Oak", 200.0, 365)
    print("Created: ", end="")
    plant2.show()

    plant3: Plant = Plant("Cactus", 5.0, 90)
    print("Created: ", end="")
    plant3.show()

    plant4: Plant = Plant("Sunflower", 80.0, 45)
    print("Created: ", end="")
    plant4.show()

    plant5: Plant = Plant("Fern", 15.0, 120)
    print("Created: ", end="")
    plant5.show()
