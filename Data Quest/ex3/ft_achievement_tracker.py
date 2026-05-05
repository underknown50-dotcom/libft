import random

ACHIEVEMENTS = [
    "First Steps",
    "Boss Slayer",
    "Treasure Hunter",
    "Master Explorer",
    "Crafting Genius",
    "World Savior",
    "Speed Runner",
    "Untouchable",
    "Collector Supreme",
    "Strategist",
    "Survivor",
    "Unstoppable",
    "Sharp Mind",
    "Hidden Path Finder",
]

PLAYERS = [
    "Alice",
    "Bob",
    "Charlie",
    "Dylan",
]


def print_header() -> None:
    print("=== Achievement Tracker System ===")


def gen_player_achievements() -> set[str]:
    achievements_count = random.randint(3, 8)
    player_achievements: set[str] = set()
    while len(player_achievements) < achievements_count:
        achievement = random.choice(ACHIEVEMENTS)
        player_achievements.add(achievement)
    return player_achievements


def create_players() -> dict[str, set[str]]:
    players: dict[str, set[str]] = {}
    for player in PLAYERS:
        players[player] = gen_player_achievements()
    return players


def print_player_achievements(players: dict[str, set[str]]) -> None:
    for player in players:
        print("Player " + player + ":", players[player])


def get_all_distinct_achievements(players: dict[str, set[str]]) -> set[str]:
    all_achievements: set[str] = set()
    for player in players:
        all_achievements = all_achievements.union(players[player])
    return all_achievements


def get_common_achievements(players: dict[str, set[str]]) -> set[str]:
    common_achievements = set(ACHIEVEMENTS)
    for player in players:
        common_achievements = common_achievements.intersection(
            players[player]
        )
    return common_achievements


def get_other_players_achievements(
    players: dict[str, set[str]],
    current_player: str,
) -> set[str]:
    other_achievements: set[str] = set()
    for player in players:
        if player != current_player:
            other_achievements = other_achievements.union(players[player])
    return other_achievements


def print_unique_achievements(players: dict[str, set[str]]) -> None:
    for player in players:
        other_achievements = get_other_players_achievements(
            players,
            player,
        )
        unique_achievements = players[player].difference(
            other_achievements
        )
        print("Only " + player + " has:", unique_achievements)


def print_missing_achievements(players: dict[str, set[str]]) -> None:
    all_possible_achievements = set(ACHIEVEMENTS)
    for player in players:
        missing_achievements = all_possible_achievements.difference(
            players[player]
        )
        print(player + " is missing:", missing_achievements)


def main() -> None:
    print_header()

    players = create_players()

    print_player_achievements(players)

    all_distinct_achievements = get_all_distinct_achievements(players)
    common_achievements = get_common_achievements(players)

    print("All distinct achievements:", all_distinct_achievements)
    print("Common achievements:", common_achievements)

    print_unique_achievements(players)
    print_missing_achievements(players)


if __name__ == "__main__":
    main()
