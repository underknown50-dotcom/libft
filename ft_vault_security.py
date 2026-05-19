import os
from typing import Tuple, Union, Optional


def normalize_action(action: Union[str, int]) -> str:
    if isinstance(action, str):
        low = action.lower()
        if low in ('r', 'read'):
            return 'r'
        if low in ('w', 'write'):
            return 'w'
    elif isinstance(action, int):
        return 'r' if action == 0 else 'w'
    return ''


def read_file_safe(filename: str) -> Tuple[bool, str]:
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return (True, content)
    except OSError as e:
        return (False, str(e))


def write_file_safe(filename: str, content: str) -> Tuple[bool, str]:
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return (True, "Content successfully written to file")
    except OSError as e:
        return (False, str(e))


def secure_archive(
    filename: str,
    action: Union[str, int] = 'r',
    content: Optional[str] = None
) -> Tuple[bool, str]:
    mode = normalize_action(action)
    if not mode:
        return (False, f"Invalid action: {action}. Use 'r' or 'w'.")

    if mode == 'r':
        return read_file_safe(filename)
    else:  # mode == 'w'
        if content is None:
            return (False, "Write action requires content parameter.")
        return write_file_safe(filename, content)


def demo_nonexistent_file() -> None:
    result = secure_archive('/not/existing/file', 'r')
    print(f"Using 'secure_archive' to read from a nonexistent file: {result}")


def demo_inaccessible_file() -> None:
    result = secure_archive('/etc/master.passwd', 'r')
    print(f"Using 'secure_archive' to read from an inaccessible file: {result}")


def demo_read_regular_file() -> None:
    test_content = (
        "[FRAGMENT 001] Digital preservation protocols established 2087\n"
        "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
        "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
    )

    secure_archive('temp_read_test.txt', 'w', test_content)

    result = secure_archive('temp_read_test.txt', 'r')
    print(f"Using 'secure_archive' to read from a regular file: {result}")

    try:
        os.remove('temp_read_test.txt')
    except OSError:
        pass


def demo_write_new_file() -> None:
    test_content = (
        "[FRAGMENT 001] Digital preservation protocols established 2087\n"
        "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
        "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
    )

    result = secure_archive('new_archive.txt', 'w', test_content)
    print(f"Using 'secure_archive' to write previous content to a new file: {result}")

    # Cleanup
    try:
        os.remove('new_archive.txt')
    except OSError:
        pass


def main() -> None:
    print("== Cyber Archives Security ==")
    demo_nonexistent_file()
    demo_inaccessible_file()
    demo_read_regular_file()
    demo_write_new_file()


if __name__ == "__main__":
    main()
