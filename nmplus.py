# create CLI wrapper for nmcli with Rich
from rich.console import Console
from rich.table import Table
from rich import box
from rich.prompt import Prompt

import subprocess
import re

console = Console()
main_color = "bold blue"


def main():
    console.print("Network Manager+ CLI", style=main_color)
    console.print("Version 0.1", style=main_color)
    console.print("Author: DanniSec", style=main_color)

    while True:
        console.print("Main Menu", style=main_color)
        console.print("1. List all connections")
        console.print("2. List all devices")
        console.print("3. List all access points")
        console.print("4. List all wireless networks")
        console.print("5. Connect to a network")
        console.print("6. Disconnect from a network")
        console.print("7. Exit")
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
    console.print("List of connections", style=main_color)
    table = Table(show_header=True, header_style=main_color, box=box.SQUARE)
    table.add_column("Name", style=main_color)
    table.add_column("UUID", style=main_color)
    table.add_column("Type", style=main_color)
    table.add_column("Device", style=main_color)

    output = subprocess.run(["nmcli", "-t", "-f", "name,uuid,type,device", "connection", "show"], capture_output=True, text=True)
    for line in output.stdout.splitlines():
        name, uuid, _type, device = line.split(":")
        table.add_row(name, uuid, _type, device)

    console.print(table)


def list_devices():
    console.print("List of devices", style=main_color)
    table = Table(show_header=True, header_style=main_color, box=box.SQUARE)
    table.add_column("Name", style=main_color)
    table.add_column("Type", style=main_color)
    table.add_column("State", style=main_color)
    table.add_column("Driver", style=main_color)
    table.add_column("HW Address", style=main_color)

    output = subprocess.run(["nmcli", "-t", "-f", "name,type,state,driver,hwaddr", "device", "show"], capture_output=True, text=True)
    for line in output.stdout.splitlines():
        name, _type, state, driver, hwaddr = line.split(":")
        table.add_row(name, _type, state, driver, hwaddr)

    console.print(table)


def list_access_points():
    output = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True)
    console.print(output.stdout)


def list_wireless_networks():
    output = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True)
    console.print(output.stdout)


def connect_to_network():
    console.print("Connect to a network", style=main_color)
    ssid = Prompt.ask("Please enter the SSID of the network you want to connect to")
    password = Prompt.ask("Please enter the password for the network", password=True)
    output = subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], capture_output=True, text=True)
    console.print(output.stdout)


def disconnect_from_network():
    console.print("Disconnect from a network", style=main_color)
    ssid = Prompt.ask("Please enter the SSID of the network you want to disconnect from")
    output = subprocess.run(["nmcli", "device", "wifi", "disconnect", ssid], capture_output=True, text=True)
    console.print(output.stdout)

if __name__ == "__main__":
    main()
