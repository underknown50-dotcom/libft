import random
from typing import Generator


PLAYERS = [
    "alice",
    "bob",
    "charlie",
    "dylan",
]

ACTIONS = [
    "run",
    "eat",
    "sleep",
    "grab",
    "move",
    "climb",
    "swim",
    "release",
    "use",
]


def print_header() -> None:
    print("=== Game Data Stream Processor ===")


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        player = random.choice(PLAYERS)
        action = random.choice(ACTIONS)

        yield (player, action)


def print_event(index: int, event: tuple[str, str]) -> None:
    player = event[0]
    action = event[1]

    print(f"Event {index}: Player {player} did action {action}")


def build_event_list(
    event_generator: Generator[tuple[str, str], None, None],
) -> list[tuple[str, str]]:
    events = []

    for _ in range(10):
        event = next(event_generator)
        events.append(event)

    return events


def consume_event(
    events: list[tuple[str, str]],
) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        index = random.randint(0, len(events) - 1)
        event = events[index]
        events.pop(index)

        yield event


def main() -> None:
    print_header()

    event_generator = gen_event()

    for index in range(1000):
        event = next(event_generator)
        print_event(index, event)

    events = build_event_list(event_generator)
    print("Built list of 10 events:", events)

    for event in consume_event(events):
        print("Got event from list:", event)
        print("Remains in list:", events)


if __name__ == "__main__":
    main()
