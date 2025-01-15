import sys
import os
from pathlib import Path


def get_arg_path(path, cmd):
    '''
    Given the PATH environment variable contents and command to be looked for find the path and return
    '''
    all_paths = path.split(":")
    for p in all_paths:
        path = Path(p)
        try:
            for child in path.iterdir():
                if cmd == str(child.stem):
                    return str(child)
        except FileNotFoundError:
            continue
    return None


def main():
    path = os.environ.get("PATH")
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
        # split into command and args
        command = split_text[0]
        command_len = len(command)
        args = ip_text[command_len+1:]
        # exit command
        if command == "exit" and args == "0":
            break
        # echo command
        elif command == "echo":
            print(f"{args}")
        # type command
        elif command == "type":
            valid_commands = ["exit", "echo", "type"]
            if args in valid_commands:
                print(f"{args} is a shell builtin")
                continue
            # if not a valid command, check for PATH environment variable
            if not path:
                print(f"{args}: not found")
                continue
            # if PATH is set, then look for the command in the directories
            arg_path = get_arg_path(path, args)
            if arg_path:
                print(f"{args} is {arg_path}")
            else:
                print(f"{args}: not found")
        # catch all
        else:
            print(f"{ip_text}: command not found")


if __name__ == "__main__":
    main()
