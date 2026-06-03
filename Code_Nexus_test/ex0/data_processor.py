from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data to output")
        rank, value = self._storage.pop(0)
        return rank, value


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                isinstance(i, (int, float)) and not isinstance(i, bool)
                for i in data
            )
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        return False

    def ingest(
        self,
        data: int | float | list[int] | list[float] | list[int | float],
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        entries = data if isinstance(data, list) else [data]
        for item in entries:
            self._storage.append((self._rank, str(item)))
            self._rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        entries = data if isinstance(data, list) else [data]
        for item in entries:
            self._storage.append((self._rank, str(item)))
            self._rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_valid_dict(d: Any) -> bool:
            return (
                isinstance(d, dict)
                and "log_level" in d
                and "log_message" in d
                and isinstance(d["log_level"], str)
                and isinstance(d["log_message"], str)
            )

        if isinstance(data, list) and len(data) > 0:
            return all(is_valid_dict(item) for item in data)
        if isinstance(data, dict):
            return is_valid_dict(data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            formatted = (
                f"{entry['log_level']}: {entry['log_message']}"
            )
            self._storage.append((self._rank, formatted))
            self._rank += 1


if __name__ == "__main__":
    print("=== Code Nexus Data Processor ===")

    print("Testing Numeric Processor...")
    num_proc = NumericProcessor()
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    num_list = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_list}")
    num_proc.ingest(num_list)
    print("Extracting 3 values...")
    for idx in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {idx}: {val}")

    print("Testing Text Processor...")
    text_proc = TextProcessor()
    print(f"Trying to validate input '42': {text_proc.validate(42)}")
    text_list = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_list}")
    text_proc.ingest(text_list)
    print("Extracting 1 value...")
    rank, val = text_proc.output()
    print(f"Text value 0: {val}")

    print("Testing Log Processor...")
    log_proc = LogProcessor()
    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    log_data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for idx in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {idx}: {val}")
