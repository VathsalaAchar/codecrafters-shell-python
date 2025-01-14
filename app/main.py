import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    command = input()
    if command == "exit 0":
        return False
    else:
        print(f"{command}: command not found")
        return True


if __name__ == "__main__":
    while True:
        if not main():
            break
