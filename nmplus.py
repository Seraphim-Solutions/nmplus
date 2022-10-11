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
from platform import system

console = Console()
main_color = "bold blue"


def main():
    print_logo()
    
    while True:
        banner("Main Menu")
        console.print("""
1. List all connections
2. List all devices
3. List all access points
4. List all wireless networks
5. Connect to a network
6. Disconnect from a network
7. Exit
""", justify="center")
        console.print("", style=main_color)

        choice = Prompt.ask("Please choose an option", choices=["1", "2", "3", "4", "5", "6", "7"])

        if choice == "1":
            list_connections()
        elif choice == "2":
            list_devices()
        elif choice == "3":
            list_access_points()
        elif choice == "4":
            list_wireless_networks()
        elif choice == "5":
            connect_to_network()
        elif choice == "6":
            disconnect_from_network()
        elif choice == "7":
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

    output = subprocess.run(["nmcli", "-g", "GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATUS,GENERAL.DRIVER,GENERAL.HWADDR", "device", "show"], capture_output=True, text=True)
    
    y, x = 0, 6
    lines = output.stdout.splitlines()
    length = len(lines) / 6
    for _device in range(math.ceil(length)):
        name = lines[y]
        _type = lines[y + 1]
        state = lines[y + 2]
        driver = lines[y + 3]
        hwaddr = lines[y + 4]
        table.add_row(name, _type, state, driver, hwaddr)
        y += x
        x *= x 

    console.print(table, justify="center")


def list_access_points():
    banner("List of access points")
    output = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True)
    console.print(output.stdout, justify="center")


def list_wireless_networks():
    banner("List of wireless networks")
    output = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True)
    console.print(output.stdout, justify="center")


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
    height = 8
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