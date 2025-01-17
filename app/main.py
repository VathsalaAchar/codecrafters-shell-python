import sys
import os
import subprocess
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
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        ip_text = input()
        if not ip_text:
            continue
        # split text to get command and arguments
        if "'" in ip_text:
            delim = "'"
        else:
            delim = None
        split_text = [t for t in ip_text.split(delim)]
        split_text[0] = split_text[0].strip() # clean up the first argument in the split to remove spaces

        builtin_commands = ["exit", "echo", "type", "pwd", "cd"]

        match split_text:
            # exit command
            case ["exit"]:
                print("If you want to exit try: exit 0")
            case ["exit", "0"]:
                break
            # echo command
            case ["echo", *args]:
                if delim: # join with no space if there is a delimiter i.e., '
                    joined_args = ''.join(a for a in args)
                else:
                    joined_args = ' '.join(a for a in args)
                print(joined_args)
            # type command
            case ["type", cmd] if cmd in builtin_commands:
                print(f"{cmd} is a shell builtin")
            case ["type", *args]:
                args = " ".join(a.strip() for a in args)
                # look for the command in $PATH
                path = os.environ.get("PATH")
                arg_path = get_arg_path(path, args)
                if arg_path:
                    print(f"{args} is {arg_path}")
                else:
                    print(f"{args}: not found")
            # get present working directory
            case ["pwd"]:
                print(os.getcwd())
            # change directory - user's home directory
            case ["cd", "~"]:
                home_dir = os.environ.get("HOME")  # finds home dir
                os.chdir(home_dir)
            # change directory - absolute and relative paths
            case ["cd", dir_path]:
                try:
                    os.chdir(dir_path)
                except FileNotFoundError:
                    print(f"cd: {dir_path}: No such file or directory")
            # run an executable
            case [an_exe, *args]:
                args = [a for a in args if a not in ['', ' ']] # gets rid of empty/space arguments to cmd
                try:
                    subprocess.call([an_exe, *args])
                except FileNotFoundError:
                    print(f"{ip_text}: command not found")


if __name__ == "__main__":
    main()
