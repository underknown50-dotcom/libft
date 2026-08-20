def cryptic_sorter(strings: list[str]) -> list[str]:

    def count_vowels(s):
        count = 0
        for i in s.lower():
            if i in "aeiou":
                count += 1
        return count

    def should_swap(a, b):
        if len(a) != len(b):
            return len(a) > len(b)

        if a.lower() != b.lower():
            return a.lower() > b.lower()

        return count_vowels(a) > count_vowels(b)

    result = strings.copy()

    for i in range(len(result)):
        for j in range(len(result) - 1 - i):
            if should_swap(result[j], result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]

    return result
