    import sys
    
    def print_header() -> None:
        print("=== Command Quest ===")
    
    def print_program_name(program_name: str) -> None:
        print(f"Program name: {program_name}")
    
    def print_no_arguments() -> None:
        print("No arguments provided!")
    
    def print_arguments_count(count: int) -> None:
        print(f"Arguments received: {count}")
    
    def print_arguments(args: list[str]) -> None:
        for i, arg in enumerate(args, start=1):
            print(f"Argument {i}: {arg}")
    
    def print_total_arguments(total: int) -> None:
        print(f"Total arguments: {total}")
    
    def main() -> None:
        argv = sys.argv
        total_args = len(argv)
        extra_args = argv[1:]
        extra_count = len(extra_args)
    
        print_header()
        print_program_name(argv[0])
    
        if extra_count > 0:
            print_arguments_count(extra_count)
            print_arguments(extra_args)
        else:
            print_no_arguments()
    
        print_total_arguments(total_args)
    
    if __name__ == "__main__":
        main()
