import os
import subprocess
from datetime import datetime
import time
import socket

show_vendor = True

logo = """
\033[38;2;120;0;0m███╗   ██╗███████╗████████╗    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
\033[38;2;170;20;0m████╗  ██║██╔════╝╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
\033[38;2;220;50;0m██╔██╗ ██║█████╗     ██║          ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
\033[38;2;255;90;0m██║╚██╗██║██╔══╝     ██║          ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
\033[38;2;255;140;40m██║ ╚████║███████╗   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
\033[38;2;255;200;100m╚═╝  ╚═══╝╚══════╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
\033[0m
"""

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_menu():
    print(logo)
    print("[1] Scan Local Network (Nmap)")
    print("[2] Scan Ports (Socket)")
    print("[3] Configuration")
    print("[4] Info")
    print("[0] Exit")
    print()

def live_scanning():
    global show_vendor
    clear()
    print("┌────────────────────────────────────────────┐")
    print("│                PORT SCANNER                │")
    print("└────────────────────────────────────────────┘")
    print()
    print()
    print("CTRL + C to stop\n")

    network = input("Enter network (example: 192.168.xx.x/22): ")
    nmap_path = get_nmap_path()

    if nmap_path is None:
        print("\n[ERROR] Nmap not found.")
        input("\nPress Enter...")
        return

    previous = {}

    try:
        while True:
            result = subprocess.run(
                [nmap_path, "-sn", network],
                capture_output=True,
                text=True
            )

            output = result.stdout.splitlines()
            current = {}
            ip = ""
            mac = ""
            vendor = ""

            for line in output:
                line = line.strip()
                if "Nmap scan report for" in line:
                    ip = line.split()[-1]
                elif "MAC Address:" in line:
                    parts = line.split("MAC Address: ")[1]
                    mac = parts.split(" ")[0]
                    vendor = ""
                    if "(" in line:
                        vendor = line.split("(")[-1].replace(")", "")
                    current[mac if mac else ip] = (ip, mac, vendor)

            new_devices = set(current.keys()) - set(previous.keys())
            lost_devices = set(previous.keys()) - set(current.keys())

            clear()
            print("=================================")
            print("        LIVE SCANNING")
            print("=================================\n")

            if new_devices:
                print("🟢 NEW DEVICES:")
                for d in new_devices:
                    print("   ", current[d][0], current[d][1])

            if lost_devices:
                print("\n🔴 DISCONNECTED:")
                for d in lost_devices:
                    print("   ", previous[d][0], previous[d][1])

            print("\nIP               MAC               VENDOR")
            print("-" * 50)

            for d in current.values():
                ip, mac, vendor = d
                if show_vendor:
                    print(f"{ip:<16} {mac:<17} {vendor}")
                else:
                    print(f"{ip:<16} {mac:<17}")

            previous = current
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nStopped.")
        input("Press Enter to return...")

def config():
    global show_vendor
    while True:
        clear()
        status = "ON" if show_vendor else "OFF"
        print("┌────────────────────────────────────────────┐")
        print("│            SYSTEM CONFIGURATION            │")
        print("└────────────────────────────────────────────┘")
        print()
        print(f"[1] Show Vendor: {status}")
        print("[0] Return")
        print()

        option = input("Option: ")
        if option == "1":
            clear()
            print("[1] ON")
            print("[2] OFF")
            print()
            choice = input("Option: ")
            if choice == "1":
                show_vendor = True
                print("\nVendor display enabled.")
                input("\nPress Enter...")
            elif choice == "2":
                show_vendor = False
                print("\nVendor display disabled.")
                input("\nPress Enter...")
        elif option == "0":
            break

def get_nmap_path():
    possible_paths = [
        r"C:\Program Files (x86)\Nmap\nmap.exe",
        r"C:\Program Files\Nmap\nmap.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def info():
    clear()
    print("┌────────────────────────────────────────────┐")
    print("│            PROJECT INFORMATION             │")
    print("└────────────────────────────────────────────┘")
    print()
    print(f"{'NAME:':<15} Net Toolkit")
    print(f"{'VERSION:':<15} 1.0.0")
    print(f"{'CREATOR:':<15} Parsos")
    print(f"{'LANGUAGE:':<15} Python 3.x")
    print("-" * 46)
    print("CORE MODULES & DEPENDENCIES:")
    print(" • Network Scan : Nmap CLI Automation (Subprocess)")
    print(" • Port Scan    : Low-level TCP Sockets (Native)")
    print("-" * 46)
    print("REPOSITORY & LICENSING:")
    print(" • License      : MIT License")
    print(" • Purpose      : Educational & Portfolio Project")
    print()
    input("Press Enter To Return To Main Menu...")

def scan_network():
    global show_vendor
    clear()
    print("┌────────────────────────────────────────────┐")
    print("│            NETWORK SCANNER TOOL            │")
    print("└────────────────────────────────────────────┘")
    print()
    print("[1] Scan Network")
    print("[2] Live Scanning")
    print("[0] Return")
    print(" ")

    x = input("Option: ")
    if x == "1":
        network = input("Enter network (example: 192.168.xx.x/22): ")
        nmap_path = get_nmap_path()

        if nmap_path is None:
            print("\n[ERROR] Nmap was not found.")
            input("\nPress Enter...")
            return

        clear()
        print("Scanning...\n")

        result = subprocess.run(
            [nmap_path, "-sn", network],
            capture_output=True,
            text=True
        )

        output = result.stdout.splitlines()
        devices = []
        ip = ""
        mac = ""
        vendor = ""

        for line in output:
            line = line.strip()
            if "Nmap scan report for" in line:
                ip = line.split()[-1]
            elif "MAC Address:" in line:
                parts = line.split("MAC Address: ")[1]
                mac_part = parts.split(" ")[0]
                mac = mac_part
                if "(" in line:
                    vendor = line.split("(")[-1].replace(")", "")
                devices.append((ip, mac, vendor))

        print("IP               MAC               VENDOR")
        print("-" * 50)

        for d in devices:
            ip, mac, vendor = d
            if show_vendor:
                print(f"{ip:<16} {mac:<17} {vendor}")
            else:
                print(f"{ip:<16} {mac:<17}")

        print()
        sn = input("Do you want to save the report? (S/N): ").lower()

        if sn == "s":
            folder = input("Choose a folder to save the report: ")
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"network_report_{now}.txt"
            file_path = os.path.join(folder, file_name)

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("IP               MAC               VENDOR\n")
                    f.write("-" * 50 + "\n")
                    for d in devices:
                        ip, mac, vendor = d
                        if show_vendor:
                            f.write(f"{ip:<16} {mac:<17} {vendor}\n")
                        else:
                            f.write(f"{ip:<16} {mac:<17}\n")
                print("\nReport saved successfully!")
                print(file_path)
            except Exception as e:
                print(f"\n[ERROR] Could not save file: {e}")
            input("\nPress Enter...")
        else:
            input("\nPress Enter...")
    elif x == "2":
        live_scanning()



def execute_port_scan(target, ports):
    """Ejecuta la conexión socket real hacia los puertos dados."""
    print(f"\nEscaneando objetivo: {target}...\n")
    try:
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)  # Optimizado el tiempo de espera
            result = s.connect_ex((target, port))

            if result == 0:
                print(f" Puerto {port:<5}: \033[92mABIERTO\033[0m")
            else:
                # Opcional: imprimir los cerrados o ignorarlos para no saturar la pantalla
                print(f" Puerto {port:<5}: \033[91mCERRADO\033[0m")
            s.close()
    except KeyboardInterrupt:
        print("\n[!] Escaneo cancelado por el usuario.")

def scan_rapido():
    clear()
    print("=== SCAN RÁPIDO ===")
    target = input("IP objetivo: ")
    ports = [22, 80, 443, 3306, 8080]
    execute_port_scan(target, ports)
    input("\nENTER para volver...")

def scan_completo():
    clear()
    print("=== SCAN COMPLETO (1-1000) ===")
    target = input("IP objetivo: ")
    print("\nEscaneando... Esto puede tardar un momento.\n")
    
    # Para el completo, mostramos solo los ABIERTOS para mantener la consola limpia
    try:
        for port in range(1, 1001):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f" Puerto {port:<5}: \033[92mABIERTO\033[0m")
            s.close()
    except KeyboardInterrupt:
        print("\n[!] Escaneo cancelado.")
        
    input("\nENTER para volver...")

def scan_personalizado():
    clear()
    print("=== SCAN PERSONALIZADO ===")
    target = input("IP objetivo: ")
    puertos = input("Puertos separados por coma (ej: 80,443,22): ")

    try:
        # Sanitización de datos limpia eliminando espacios vacíos
        ports = [int(p.strip()) for p in puertos.split(",") if p.strip().isdigit()]
        if not ports:
            print("\n[ERROR] No ingresaste puertos válidos.")
        else:
            execute_port_scan(target, ports)
    except Exception as e:
        print(f"\n[ERROR] Entrada inválida: {e}")

    input("\nENTER para volver...")

def info_host():
    clear()
    print("=== INFO DEL HOST ===")
    target = input("IP o dominio: ")

    try:
        ip = socket.gethostbyname(target)
        print(f"\nHost: {target}")
        print(f"IP: {ip}")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"Hostname: {hostname}")
        except socket.herror:
            print("Hostname: no encontrado (Reverse DNS falló)")
    except socket.gaierror:
        print("\n[ERROR] No se pudo resolver el host. Verifica la conexión o el dominio.")

    input("\nENTER para volver...")

def ports_menu():
    """Muestra el submenú de puertos sin colisionar en nombre ni recursividad."""
    while True:
        clear()
        print("┌────────────────────────────────────────────┐")
        print("│             PORT SCANNER MENU              │")
        print("└────────────────────────────────────────────┘")
        print("[1] Scan rápido")
        print("[2] Scan completo")
        print("[3] Scan personalizado")
        print("[4] Info del host")
        print("[0] Volver al Menú Principal")
        print("")

        x = input("Option: ")

        if x == "1":
            scan_rapido()
        elif x == "2":
            scan_completo()
        elif x == "3":
            scan_personalizado()
        elif x == "4":
            info_host()
        elif x == "0":
            return  # Rompe la función de forma limpia regresando al main
        else:
            print("Opción inválida")
            time.sleep(1)




def main():
    while True:
        clear()
        show_menu()

        option = input("Select option: ")

        if option == "1":
            scan_network()
        elif option == "2":
            ports_menu()  # Nombre actualizado correctamente
        elif option == "3":
            config()
        elif option == "4":
            info()
        elif option == "0":
            print("\nExiting...")
            break
        else:
            print("\nInvalid option.")
            input("Press Enter...")

if __name__ == "__main__":
    main()

