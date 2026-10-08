import shlex

from service import MiniGit


def execute(command, count, func):
    if isinstance(count, int): count = (count,)

    if len(command) not in count:
        print("Invalid args")
        return

    func(*command[1:])


def main():
    git = MiniGit()

    while True:
        try:
            value   = input("mini-git> ")
            command = shlex.split(value)

            if not command: continue

            raw_command = command[0]
            command[0]  = command[0].upper()

            if command[0] in ("EXIT", "QUIT"): break

            if   command[0] == "INIT"      : execute(command, 2,      git.INIT)
            elif command[0] == "BRANCH"    : execute(command, 2,      git.BRANCH)
            elif command[0] == "SWITCH"    : execute(command, 2,      git.SWITCH)
            elif command[0] == "COMMIT"    : execute(command, 2,      git.COMMIT)

            elif command[0] == "LOG"       : execute(command, (1, 2), git.LOG)
            elif command[0] == "PATH"      : execute(command, 3,      git.PATH)
            elif command[0] == "ANCESTORS" : execute(command, 2,      git.ANCESTORS)
            elif command[0] == "SEARCH"    : execute(command, 2,      git.SEARCH)

            else: print(f"Unknown command: {raw_command}")

        except ValueError: print("Invalid args")

if __name__ == "__main__":
    main()