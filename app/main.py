import sys
import os
import subprocess
from shlex import split


def get_arg_path(path, cmd):
    '''
    Given the PATH environment variable contents and command to be looked for find the path and return
    '''
    all_paths = path.split(":")
    for dir_path in all_paths:
        poss_exe_path = os.path.join(dir_path, cmd)
        try:
            if os.stat(poss_exe_path):
                return poss_exe_path
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
        split_text = split(ip_text)

        builtin_commands = ["exit", "echo", "type", "pwd", "cd"]

        match split_text:
            # exit command
            case ["exit"]:
                print("If you want to exit try: exit 0")
            case ["exit", "0"]:
                break
            # echo command
            case ["echo", *args]:
                print(*args)
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
                try:
                    subprocess.call([an_exe, *args])
                except FileNotFoundError:
                    print(f"{ip_text}: command not found")


if __name__ == "__main__":
    main()
