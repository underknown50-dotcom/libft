import random

PLAYERS = [
    "Alice",
    "bob",
    "Charlie",
    "dylan",
    "Emma",
    "Gregory",
    "john",
    "kevin",
    "Liam",
]

MIN_SCORE = 0
MAX_SCORE = 1000


def print_header() -> None:
    print("=== Game Data Alchemist ===")


def get_capitalized_players(players: list[str]) -> list[str]:
    return [player.capitalize() for player in players]


def get_only_originally_capitalized(players: list[str]) -> list[str]:
    return [player for player in players if player[0].isupper()]


def build_score_dict(players: list[str]) -> dict[str, int]:
    return {player: random.randint(MIN_SCORE, MAX_SCORE) for player in players}


def get_high_scores(scores: dict[str, int], average: float) -> dict[str, int]:
    return {
        player: score
        for player, score in scores.items()
        if score > average
    }


def main() -> None:
    print_header()

    print("Initial list of players:", PLAYERS)

    all_capitalized = get_capitalized_players(PLAYERS)
    print("New list with all names capitalized:", all_capitalized)

    only_capitalized = get_only_originally_capitalized(PLAYERS)
    print("New list of capitalized names only:", only_capitalized)

    score_dict = build_score_dict(all_capitalized)
    print("Score dict:", score_dict)

    average_score = sum(score_dict.values()) / len(score_dict)
    print(f"Score average is {average_score:.2f}")

    high_scores = get_high_scores(score_dict, average_score)
    print("High scores:", high_scores)


if __name__ == "__main__":
    main()
