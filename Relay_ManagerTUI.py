"""
The TUI part of Relay Manager. Please do not read the code.
This is one of the most unreadable thing i've produced.
"""

# ANSI escape codes

cyan, reset = "\033[36m", "\033[0m"
gray = "\033[37m"
dark_green, red, yellow, dim = "\033[32m", "\033[31m", "\033[33m", "\033[2m"
bold = "\033[1m"
green = "\033[92m"


# Box setup

edge = f"━"*95
BTL, BTR, BDL, BDR, LN = "┏", "┓", "┗", "┛", "━"    # Stands for Box Top left, top right, down left and down right
upper, lower, sides = f"┏{edge}┓",f"┗{edge}┛", "┃"



art = [
    r"                                                                                               ",
    r"      _____  __   __  _____      _               __  __                                        ",
    r"     |  __ \ \ \ / / |  __ \    | |             |  \/  |                                       ",
    r"     | |__) | \ V /  | |__) |___| | __ _ _   _  | \  / | __ _ _ __   __ _  __ _  ___ _ __      ",
    r"     |  _  /   > <   |  _  // _ \ |/ _` | | | | | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|     ",
    r"     | | \ \  / Λ \  | | \ \  __/ | (_| | |_| | | |  | | (_| | | | | (_| | (_| |  __/ |        ",
    r"     |_|  \_\/_/ \_\ |_|  \_\___|_|\__,_|\__, | |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|        ",
    r"                                          __/ |                            __/ |               ",
    r"                                         |___/                            |___/                ",
    r"                                                                                               ",
    r"               Routing encrypted messages over a De-centralized Relay overlay.                "
]




def pad_line_art(line, width):
    return line + " "*(width - len(line))

def ascii_boxed_art(ascii_lines, boxwidth=95):
    print(dim+upper+reset)
    for line in ascii_lines:
        print(f"{dim}{sides}{reset}{cyan}{pad_line_art(line, boxwidth)}{reset}{dim}{sides}{reset}")
    print(dim+lower+reset)

def intro_screen():
    ascii_boxed_art(art)

def pad(val, width, char=" "):
    return str(val).ljust(width, char)
def show_status(service: str, status: str, substate: str, pid: int, cpu_sec: int,mem_usage: int, cpu_usage: int):
    box_side = f"{dim}{sides}{reset}"
    return (fr"""
    {dim}{BTL}{LN*2} {service} Status {LN*28}{BTR}{reset}
    {box_side}                                             {box_side}
    {box_side}{cyan}   {bold}Status{reset}      :      {green}{pad(status, 23)}{reset}{box_side}
    {box_side}{cyan}   {bold}State{reset}       :      {pad(substate, 23)}{box_side}
    {box_side}{cyan}   {bold}PID{reset}         :      {pad((pid if pid != "0" else "Inactive"), 23)}{box_side}
    {box_side}{cyan}   {bold}Started{reset}     :      {pad((f"Started {cpu_sec}s ago." if cpu_sec else "Inactive"), 23)}{box_side}
    {box_side}{cyan}   {bold}Memory{reset}      :      {cyan}{pad((f"Using {mem_usage} MB of RAM." if mem_usage != 0 else "Inactive"), 23)}{reset}{box_side}
    {box_side}{cyan}   {bold}CPU{reset}         :      {cyan}{pad((f"Using {cpu_usage}% of CPU."), 23)}{reset}{box_side}
    {box_side}                                             {box_side}
    {dim}{BDL}{LN*45}{BDR}{reset}
    """)

def show_options():
    side = f"{dim}┃{reset}"
    
    print(f"""
    {dim}┏━━{bold}{cyan} Commands {reset}{dim}{LN*30}┓{reset}
    {side}                                          {side}
    {side}    {green}[st]{reset}{cyan} Status{reset}         {green}[sp]{reset}{cyan} Stop{reset}         {side}
    {side}    {green}[rp]{reset}{cyan} Repair{reset}         {green}[sd]{reset}{cyan} Shutdown{reset}     {side}
    {side}    {green}[lg]{reset}{cyan} Logs{reset}           {green}[re]{reset}{cyan} Restart{reset}      {side}
    {side}    {green}[up]{reset}{cyan} Update{reset}         {green}[rm]{reset}{cyan} Uninstall{reset}    {side}
    {side}                                          {side}
    {side}{" "*14}{dim}{bold}{cyan}-- Utility --{reset}{" "*15}{side}
    {side}                                          {side}
    {side}{" "*8}{green}help, exit, art, commands{reset}{" "*9}{side}
    {dim}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
    """)

def show_args(command_name):
    side = f"{dim}┃{reset}"
    print(f"""
    {dim}┏━━{reset} {bold+cyan}{"Arguments"} {reset}{dim}━━━━━━━━━━━━━━━━━━━━━━━┓
    {side}                                    {side}
    {side}{dim+gray+bold}  » Command name: {cyan}{pad(command_name, 18)}{reset}{side}
    {side}                                    {side}
    {side}   {green}[1]{reset}{gray} Tor{reset}             {green}[2]{reset} {gray}Relay{reset}    {side}
    {side}                                    {side}
    {dim}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
    """)