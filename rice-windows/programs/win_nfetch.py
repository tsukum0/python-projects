import os
import sys
import subprocess
import time

os.system('title ')

mostrar_ip = 0  # mude para 1 se quiser mostrar o ip!

# Dependências necessárias
REQUIRED_LIBS = ["rich", "psutil"]

def in_venv():
    return sys.prefix != sys.base_prefix

def relaunch_in_venv():
    python = os.path.join("venv", "Scripts", "python")
    os.execv(python, [python, __file__])

# Auto setup venv
if not in_venv():
    relaunch_in_venv()

# Importações após venv estar ativo
import msvcrt
import platform
import psutil
import socket
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

console = Console()

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return str(uptime).split('.')[0]

def get_ip():
    hostname = socket.gethostname()
    if mostrar_ip == 1:
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            ip = "N/A"
        return ip
    else:
        return "---.---.--.--"

def show_info():
    os.system("cls")

    uname = platform.uname()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    ascii_logo = Text.from_ansi("""\033[31m
                   .oodMMMMMMMMMMMMM
       ..oodMMM  MMMMMMMMMMMMMMMMMMM
 oodMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 MMMMMMMMMMMMMM  MMMMMMMMMMMMMMMMMMM
 `^^^^^^MMMMMMM  MMMMMMMMMMMMMMMMMMM
       ````^^^^  ^^MMMMMMMMMMMMMMMMM
                      ````^^^^^^MMMM\033[0m
""")

    info = Table.grid(padding=1)
    info.add_row("Hostname:", uname.node)
    info.add_row("OS:", f"{uname.system} {uname.release}")
    info.add_row("Kernel:", uname.version)
    info.add_row("Uptime:", get_uptime())
    info.add_row("CPU:", platform.processor())
    info.add_row("Memory:", f"{mem.used // (1024**2)} MiB / {mem.total // (1024**2)} MiB")
    info.add_row("Disk:", f"{disk.used // (1024**3)} GiB / {disk.total // (1024**3)} GiB")
    info.add_row("IP:", get_ip())
    info.add_row("Python:", platform.python_version())

    panel = Panel(info, border_style="red", title="[bold red]System Info[/]")
    columns = Columns([ascii_logo, panel], equal=False, expand=True, padding=(0, 0))

    console.print(columns)
    console.print("\n[bold red]Pressione enter 2x para atualizar...[/]")

def main():
    while True:
        show_info()
        msvcrt.getch()  # Espera qualquer tecla

if __name__ == "__main__":
    main()
