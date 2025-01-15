import sys


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        ip_text = input()
        if not ip_text:
            continue
        # split text to get command and arguments
        split_text = ip_text.split()
        if len(split_text) == 1:
            print(f"{ip_text}: command not found")
            continue

        command = split_text[0]
        command_len = len(command)
        args = ip_text[command_len+1:]

        if command == "exit" and args == "0":
            break
        elif command == "echo":
            print(f"{args}")
        elif command == "type":
            if args in ["exit", "echo", "type"]:
                print(f"{args} is a shell builtin")
            else:
                print(f"{args}: not found")
        else:
            print(f"{ip_text}: command not found")


if __name__ == "__main__":
    main()
