import sys


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        ip_text = input()

        if ip_text == "exit 0":
            break
        elif ip_text.split()[0] == "echo":
            command = ip_text.split()[0]
            args = ip_text[5:]
            print(f"{args}")
        else:
            print(f"{ip_text}: command not found")


if __name__ == "__main__":
    main()
