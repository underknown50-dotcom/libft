import sys


USAGE_MESSAGE = (
    "No scores provided. Usage: "
    "python3 ft_score_analytics.py <score1> <score2> ..."
)


def print_header() -> None:
    print("=== Player Score Analytics ===")


def print_usage() -> None:
    print(USAGE_MESSAGE)


def convert_to_score(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        print(f"Invalid parameter: '{value}'")
        return None


def parse_scores(arguments: list[str]) -> list[int]:
    scores = []
    for arg in arguments[1:]:
        score = convert_to_score(arg)
        if score is not None:
            scores.append(score)
    return scores


def print_score_analytics(scores: list[int]) -> None:
    if not scores:
        print("No valid scores to analyze.")
        return
    
    total_score = sum(scores)
    high_score = max(scores)
    low_score = min(scores)
    average_score = total_score / len(scores)

    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total_score}")
    print(f"Average score: {average_score}")
    print(f"High score: {high_score}")
    print(f"Low score: {low_score}")
    print(f"Score range: {high_score - low_score}")


def main() -> None:
    arguments = sys.argv

    print_header()

    if len(arguments) == 1:
        print_usage()
        return

    scores = parse_scores(arguments)

    if len(scores) == 0:
        print_usage()
        return

    print_score_analytics(scores)


if __name__ == "__main__":
    main()
