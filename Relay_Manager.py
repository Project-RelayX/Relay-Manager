import subprocess, time

from Relay_ManagerTUI import show_status, show_args

clear_screen = "\033[2J\033[H"
hide_cursor = "\033[?25l"
show_cursor = "\033[?25h"
reset = "\033[36m", "\033[0m"
green, red, yellow, dim = "\033[32m", "\033[31m", "\033[33m", "\033[2m"

running = True
def clean_up():
    print(reset + show_cursor, end="", flush=True)

def handle_exit():
    clean_up()
    running = False

def systemctl_info(service, *properties):
    cmd = ["systemctl" "show", service, "--no-page", "--property=" ",".join(properties)]
    try:
        out = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError:
        return {}
    data = {}
    for line in out.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key] = value
    return data

def service_status(service):
    data = systemctl_info(
        service, "ActiveState", "Substate", "ExecMainPID", 
        "MemoryCurrent", "CPUUsageNSec", "ActiveTimestampMonotonic"
    )
    active = data.get("ActiveState") == "active"
    sub = data.get("SubState", "Unknown")
    pid = data.get("ExecMainPID", "0")
    mem = int(data.get("MemoryCurrent", "0")) // (1024*1024)
    cpu_ns = int(data.get("CPUUsageNSec", "0"))
    return {
        "active" : active,
        "sub" : sub,
        "pid" : pid,
        "mem_mb" : mem,
        "cpu_sec" : cpu_ns / 1e9
    }

def cpu_usage(pid):
    out = subprocess.check_output(["ps", "-p", str(pid), "-o", "%cpu"])
    return float(out)

def format_status(ok, text):
    if ok:
        return green + text + reset
    return red + text + reset


def fetch_status(service):
    print(hide_cursor, end="", flush=True)
    while running:
        data = service_status(service)
        ok_1, status = data["active"], "Active" if data["active"] else "Inactive"
        substate, ok_2 = data["sub"], True if data["sub"] != "Unknown" else False
        pid = data["pid"] if pid != "0" else "Inactive"
        mem = data["mem_mb"] if data["mem_mb"] != 0 else "Not running."
        cpu_sec = data["cpu_sec"] if data["cpu_sec"] else "Not running."
        if isinstance(pid, int):
            cpu_use = cpu_usage(pid)
        else:
            cpu_use = "Not running."
        print(clear_screen, end="")
        print(show_status(service,
            format_status(ok_1, status), format_status(ok_2, substate),
            pid, cpu_sec, mem, cpu_use), flush=True)
        time.sleep(1.5)
    clean_up()

def parse_command(user_input: str, arg_commands: dict, single_line_commands: dict):
    """user_input must be lowercase"""
    try:
        if len(user_input) == 1:
            if user_input[0][:2] in arg_commands:
                show_args(user_input[0])
                arg = input("Relay-Manager> ")
                if arg == "1" or arg == "2":
                    arg="tor" if arg=="1" else "relay"
                return arg_commands[user_input[0][:2]](arg)
            elif user_input[0][:2] in single_line_commands:
                return single_line_commands[user_input[0][:2]]()
            else:
                print(f"Invalid command '{user_input[0]}'. Type 'help' for a list of commands. ")
        elif len(user_input) > 1:
            return arg_commands[user_input[0][:2]](" ".join(user_input[1:]))
    except KeyError:
        print(f"Invalid command '{user_input[0]}' with argument '{user_input[1]}'. Type 'help' for a list of commands.")
