import sys
import os
import subprocess
import re
from typing import Tuple, List


def get_arg_path(path: str, cmd: str) -> str | None:
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


def split_cmd_args(user_input: str) -> List[str | None]:
    cmd_args = user_input.split(" ", maxsplit=1)
    cmd = cmd_args[0]
    # add command to the return list
    split_text = []
    split_text.append(cmd)
    args_to_split = None
    if len(cmd_args) > 1:
        args_to_split = cmd_args[1:][0]
    # if there are no arguments append command with None and return
    if not args_to_split:
        split_text.append(None)
        return split_text
    # split arguments
    if args_to_split.startswith("'"):
        # remove single quotes
        args_split_quotes = args_to_split.split("'")
        args_to_split = [a for a in args_split_quotes if a != ""]
    elif args_to_split.startswith('"'):
        # remove double quotes
        args_split_quotes = args_to_split.split('"')
        if cmd == "echo":
            ans = ""
            for a in args_split_quotes:
                if a == "":
                    continue
                elif a.strip() == "":
                    ans += " "
                else:
                    ans += a
            args_to_split = [ans]
        else:
            args_to_split = [
                a for a in args_split_quotes if a.strip() != ""]
    elif "\\" in args_to_split:
        re_backslash = re.compile(r"\\*(\w*\s*)")
        args_split_backslash = re_backslash.split(args_to_split)
        if cmd == "echo":
            ans = ""
            for a in args_split_backslash:
                if a != "":
                    ans += a
            args_to_split = [ans]
        else:
            args_to_split = [
                a for a in args_split_backslash if a.strip() != ""]
    else:
        args_to_split = args_to_split.split(" ")
    split_text.extend(args_to_split)

    return split_text


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        ip_text = input()
        if not ip_text:
            continue

        # split text to get command and arguments
        # split_text = shlex.split(ip_text) # uses builtin method
        split_text = split_cmd_args(ip_text)

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
