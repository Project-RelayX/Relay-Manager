"""
The TUI part of Relay Manager. Please do not read the code.
This is one of the most unreadable thing i've produced.
"""
import pydoc, os

# ANSI escape codes

cyan, reset = "\033[36m", "\033[0m"
gray = "\033[37m"
dark_green, red, yellow, dim = "\033[32m", "\033[31m", "\033[33m", "\033[2m"
bold = "\033[1m"
green = "\033[92m"
edge="━"*95
upper, lower, sides = f"┏{edge}┓",f"┗{edge}┛", "┃"

# Box setup

edge = f"━"*95
BTL, BTR, BDL, BDR, LN = "┏", "┓", "┗", "┛", "━"    # Stands for Box Top left, top right, down left and down right




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

def show_status(service: str, status: str, substate: str, pid: int, cpu_sec: float,mem_usage: float, cpu_usage: float, ts : str):
    box_side = f"{dim}{sides}{reset}"
    return (fr"""
{dim}{BTL}{LN*2} {pad((service + " Status "), 14, char=LN)}{LN*35}{BTR}{reset}
{box_side}                                                    {box_side}
{box_side}{cyan}   {bold}Status{reset}      :      {green}{pad(status, 39)}{reset}{box_side}
{box_side}{cyan}   {bold}State{reset}       :      {pad(substate, 39)}{box_side}
{box_side}{cyan}   {bold}PID{reset}         :      {pad((pid if pid != "0" else "Inactive"), 30)}{box_side}
{box_side}{cyan}   {bold}CPU Time{reset}    :      {pad((f"{cpu_sec}s" if cpu_sec else "Inactive"), 30)}{box_side}
{box_side}{cyan}   {bold}Memory{reset}      :      {cyan}{pad((f"Using {mem_usage} MB of RAM." if mem_usage != 0 else "Inactive"), 30)}{reset}{box_side}
{box_side}{cyan}   {bold}CPU{reset}         :      {cyan}{pad((f"Using {cpu_usage}% of CPU."), 30) if cpu_usage != "Not Running." else {pad("Inactive", 30)}}{reset}{box_side}
{box_side}{cyan}   {bold}Uptime{reset}      :      {cyan}{pad(f"Started {ts} ago.", 30) if ts != 0 else {pad("Not Running.", 30)}}{reset}{box_side}
{box_side}                                                    {box_side}
{dim}{BDL}{LN*52}{BDR}{reset}
    """)

def show_options():
    side = f"{dim}┃{reset}"
    print(f"""
{dim}┏━━{bold}{cyan} Commands {reset}{dim}{LN*30}┓{reset}
{side}                                          {side}
{side}    {green}[st]{reset}{cyan} Status{reset}         {green}[sp]{reset}{cyan} Stop{reset}         {side}
{side}    {green}[rp]{reset}{cyan} Repair{reset}         {green}[sd]{reset}{cyan} Shutdown{reset}     {side}
{side}    {green}[lg]{reset}{cyan} Logs{reset}           {green}[re]{reset}{cyan} Restart{reset}      {side}
{side}    {green}[up]{reset}{cyan} Update{reset}         {green}[un]{reset}{cyan} Uninstall{reset}    {side}
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

def show_help():
    side = f"{dim}┃{reset}"
    help_text = f"""

    {dim}┏━━{reset+cyan+bold} Pager controls{reset}{dim} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{reset}
    {side}                                                         {side}
    {side}   Exit pager mode       :      type 'q'                 {side}
    {side}   search a term         :      /<search_text>           {side}
    {side}   Move                  :      Arrow keys               {side}
    {side}   Pager mode help       :      type 'help' and enter    {side}
    {side}                                                         {side}
    {dim}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
       
    {dim}┏━━{reset+cyan+bold} Manager Commands - Help{reset}{dim} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{reset}         
    {side}                                                                                        {side}
    {side}   {green+dim}Note: Commands accept abbreviatons or full names. Inputs are case insensitive.{reset}       {side}
    {side}                                                                                        {side}
    {side}   Utility commands ->                                                                  {side}
    {side}   {red}These commands have no abbreviations / shortcuts.{reset}                                    {side}
    {side}                                                                                        {side}
    {side}   {green}1. help{reset}        :     Shows this screen                                               {side}
    {side}   {green}2. exit{reset}        :     Exit the manager. (Does not shutdown relay / tor)               {side}
    {side}   {green}3. art{reset}         :     Prints the splash ascii art.                                    {side}
    {side}   {green}4. clear{reset}       :     clears the terminal screen.                                     {side}
    {side}   {green}5. commands{reset}    :     Prints the available commands box.                              {side}
    {side}                                                                                        {side}
    {side}   {bold+cyan}Manager commands ->{reset}                                                                  {side}
    {side}                                                                                        {side}
    {side}    1. Status{dim} ---------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}st (or) status{reset}                                                    {side}
    {side}      {cyan}Arguments{reset}   :   relay / tor                                                       {side}
    {side}      {cyan}Description{reset} :   Shows an updating dashboard of the chosen service (relay/tor).    {side}
    {side}      {cyan}Source{reset}      :   Data fetched from systemd systemctl.                              {side}
    {side}      {cyan}Example use{reset} :   st relay (or) status relay  /  st tor (or) status tor             {side}
    {side}                                                                                        {side}
    {side}    2. Repair{dim} ---------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}rp (or) repair{reset}                                                    {side}
    {side}      {cyan}Arguments{reset}   :   No arguments.                                                     {side}
    {side}      {cyan}Description{reset} :   Repairs all the binaries and verifies the torrc.                  {side}
    {side}      {cyan}Source{reset}      :   Binaries from the Install server, torrc from manager binary       {side}
    {side}      {cyan}Example use{reset} :   rp  /  repair                                                     {side}
    {side}                                                                                        {side}
    {side}    3. Logs{dim} -----------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}lg (or) logs{reset}                                                      {side}
    {side}      {cyan}Arguments{reset}   :   relay / tor                                                       {side}
    {side}      {cyan}Description{reset} :   Shows logs of the chosen service (tor/relay).                     {side}
    {side}      {cyan}Source{reset}      :   Tor logs - journalctl. Relay logs - File (~/relay_log.txt).       {side}
    {side}      {cyan}Example use{reset} :   lg relay (or) log relay  /  lg tor (or) log tor                   {side}
    {side}                                                                                        {side}
    {side}    4. Update{dim} ---------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}up (or) update{reset}                                                    {side}
    {side}      {cyan}Arguments{reset}   :   relay / tor                                                       {side}
    {side}      {cyan}Description{reset} :   Updates binaries of the specified service.                        {side}
    {side}      {cyan}Source{reset}      :   Binaries fetched from the Install server.                         {side}
    {side}      {cyan}Example use{reset} :   up relay (or) update relay  /  up tor (or) update tor             {side}
    {side}                                                                                        {side}
    {side}    5. Stop{dim} -----------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}sp (or) stop{reset}                                                      {side}
    {side}      {cyan}Arguments{reset}   :   relay / tor                                                       {side}
    {side}      {cyan}Description{reset} :   Stops the provided service from running.                          {side}
    {side}      {cyan}Done using{reset}  :   systemctl                                                         {side}
    {side}      {cyan}Example use{reset} :   sp relay (or) stop relay  /  sp tor (or) stop tor                 {side}
    {side}                                                                                        {side}
    {side}    6. Shutdown{dim} -------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}sd (or) shutdown{reset}                                                  {side}
    {side}      {cyan}Arguments{reset}   :   No arguments                                                      {side}
    {side}      {cyan}Description{reset} :   Shuts down tor and relay.                                         {side}
    {side}      {cyan}Done using{reset}  :   systemctl                                                         {side}
    {side}      {cyan}Example use{reset} :   sd  /  shutdown                                                   {side}
    {side}                                                                                        {side}
    {side}    7. Restart{dim} --------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}re (or) restart{reset}                                                   {side}
    {side}      {cyan}Arguments{reset}   :   relay / tor                                                       {side}
    {side}      {cyan}Description{reset} :   Restarts the provided daemon process.                             {side}
    {side}      {cyan}Done using{reset}  :   systemctl                                                         {side}
    {side}      {cyan}Example use{reset} :   re relay (or) restart relay  /  re tor (or) restart tor           {side}
    {side}                                                                                        {side}
    {side}    8. Uninstall{dim} ------------------------------------------------------------------{reset}     {side}
    {side}                                                                                        {side}
    {side}        {red}Warning : This Permanently erases Relay data and it cannot be recovered.{reset}        {side}
    {side}                                                                                        {side}
    {side}             {red}After Uninstalling Relay, please email projectrelayx@gmail.com{reset}             {side}
    {side}           {red}so that we can remove your Relay's onion address from our directory.{reset}         {side}
    {side}                                                                                        {side}
    {side}      {cyan}Command{reset}     :   {green}un (or) uninstall{reset}                                                 {side}
    {side}      {cyan}Arguments{reset}   :   No Arguments.                                                     {side}
    {side}      {cyan}Description{reset} :   Uninstalls the Relay software. (Tor and Relay incl.)              {side}
    {side}      {cyan}Done using{reset}  :   Recursive removal                                                 {side}
    {side}      {cyan}Example use{reset} :   un  /  uninstall                                                  {side}
    {side}                                                                                        {side}
    {dim}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
       """
    os.environ["PAGER"] = "less -R"
    pydoc.pager(help_text)