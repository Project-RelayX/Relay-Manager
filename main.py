from Relay_Manager import *
from Relay_ManagerTUI import *

cmds_with_args = {
    "st" : fetch_status
}
single_line_cmds = {}
util_commands = {"help":show_help, "art":intro_screen, "commands":show_options, "clear":clear}

def main():
    clear()
    intro_screen()
    show_options() 
    while True:
        try:
            cmd = input("Relay-Manager> ").lower().split()
            if cmd[0] == "exit" or cmd[0] == "quit":
                clear()
                break
            elif cmd[0] in util_commands:
                util_commands[cmd[0]]()
            else:
                parse_command(cmd, cmds_with_args, single_line_cmds)
        except KeyboardInterrupt:
            print("Type 'exit' to exit Relay Manager.")
            continue
        except Exception as e:
            print(f"An error occoured.\n{e}")
            continue


if __name__ == "__main__":
    main()