import os
import sys
import time

# Dependências necessárias (para referência)
REQUIRED_LIBS = ["rich", "psutil"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(BASE_DIR, "venv")
PYTHON_EXEC = os.path.join(VENV_PATH, "Scripts" if os.name == "nt" else "bin", "python")

# Verifica se está rodando dentro do venv
if sys.executable != PYTHON_EXEC:
    print("[ERRO] Execute este script via iniciar.bat para garantir o ambiente virtual ativo.")
    sys.exit(1)

# Agora os imports pesados, só se estiver no venv
import subprocess
import psutil
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Group, Console
from rich.text import Text

console = Console()

# ------------------- ESTILO -------------------
BORDER_COLOR = "#FF2B2B"
TEXT_COLOR = "#FF9E9E"
BAR_COLOR = "#FF6A6A"

# Cache para processos e CPU para melhorar performance
last_proc_update = 0
proc_update_interval = 5  # segundos
proc_table_cache = None

last_cpu_update = 0
cpu_update_interval = 1  # segundos
cpu_cache = None

def get_gpu_info():
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
            encoding="utf-8"
        ).strip()
        
        name, usage, mem_used, mem_total = output.split(", ")
        table = Table.grid(padding=0, expand=False)
        table.add_row(f"[bold]{name}[/]")
        table.add_row(f"Uso: {usage}%")
        table.add_row(f"VRAM: {mem_used}/{mem_total} MB")
    except Exception as e:
        table = Table.grid(padding=0)
        table.add_row("[bold red]Erro ao obter dados da GPU[/]")
        table.add_row(str(e))
    
    return Panel(table, title="[bold cyan] GPU", border_style=BORDER_COLOR, padding=(0,0))

def get_disk_info():
    disk = psutil.disk_usage('/')
    table = Table.grid(padding=0, expand=False)
    table.add_row(f"[bold]{'Total'}[/]: {disk.total // (1024 ** 3)} GiB")
    table.add_row(f"[bold]{'Used '}[/]: {disk.used // (1024 ** 3)} GiB")
    table.add_row(f"[bold]{'Free '}[/]: {disk.free // (1024 ** 3)} GiB")
    table.add_row(f"[bold]{'Usage'}[/]: {disk.percent}%")
    return Panel(table, title="[bold cyan] Disco", border_style=BORDER_COLOR, padding=(0,0))

def get_cpu_info_cached():
    global last_cpu_update, cpu_cache
    now = time.time()
    if not cpu_cache or (now - last_cpu_update) > cpu_update_interval:
        usage = psutil.cpu_percent(percpu=True, interval=None)
        table = Table.grid(padding=0, expand=False)
        for i, percent in enumerate(usage):
            bar = Progress(
                TextColumn(f"[bold]{i:02}[/]"),
                BarColumn(bar_width=15, complete_style=BAR_COLOR),
                TextColumn("[cyan]{task.percentage:>3.0f}%"),
                expand=True
            )
            bar.add_task("", total=100, completed=percent)
            table.add_row(bar)
        cpu_cache = Panel(table, title="[bold cyan] CPU", border_style=BORDER_COLOR, padding=(0,0))
        last_cpu_update = now
    return cpu_cache

def get_mem_info():
    mem = psutil.virtual_memory()
    table = Table.grid(padding=0)
    table.add_row(f"[bold]{'Total'}[/]: {mem.total // (1024 ** 2)} MiB")
    table.add_row(f"[bold]{'Used '}[/]: {mem.used // (1024 ** 2)} MiB")
    table.add_row(f"[bold]{'Free '}[/]: {mem.available // (1024 ** 2)} MiB")
    table.add_row(f"[bold]{'Usage'}[/]: {mem.percent}%")
    return Panel(table, title="[bold cyan] Memória", border_style=BORDER_COLOR)

def get_net_info():
    net = psutil.net_io_counters()
    table = Table.grid()
    table.add_row(f"[bold]Enviado   :[/] {net.bytes_sent // 1024} KB")
    table.add_row(f"[bold]Recebido  :[/] {net.bytes_recv // 1024} KB")
    table.add_row(f"[bold]Tx Packets:[/] {net.packets_sent}")
    table.add_row(f"[bold]Rx Packets:[/] {net.packets_recv}")
    return Panel(table, title="[bold cyan] Rede", border_style=BORDER_COLOR)

def get_proc_info_cached():
    global last_proc_update, proc_table_cache
    now = time.time()
    if not proc_table_cache or (now - last_proc_update) > proc_update_interval:
        proc_table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style=BORDER_COLOR,
            expand=True,
            show_lines=False,
            pad_edge=False,
        )
        proc_table.add_column("PID", justify="right", style=TEXT_COLOR, no_wrap=True)
        proc_table.add_column("Nome", justify="left", style=TEXT_COLOR, no_wrap=True)
        proc_table.add_column("CPU%", justify="right", style=TEXT_COLOR)
        proc_table.add_column("RAM%", justify="right", style=TEXT_COLOR)

        processes = sorted(
            psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
            key=lambda p: p.info['cpu_percent'] if p.info['cpu_percent'] is not None else 0,
            reverse=True
        )[:6]

        for proc in processes:
            try:
                proc_table.add_row(
                    str(proc.info['pid']),
                    str(proc.info['name'])[:18],
                    f"{proc.info['cpu_percent']:.1f}",
                    f"{proc.info['memory_percent']:.1f}"
                )
            except psutil.NoSuchProcess:
                continue

        proc_table_cache = Panel(proc_table, title="[bold cyan] Processos", border_style=BORDER_COLOR, padding=(0,0))
        last_proc_update = now
    return proc_table_cache

# ⬇️ Esquerda (GPU, Memória, Disco, Rede)
def left_column():
    return Group(
        get_gpu_info(),
        get_mem_info(),
        get_disk_info(),
        get_net_info()
    )

# ⬇️ Direita (CPU, Processos)
def right_column():
    return Group(
        get_cpu_info_cached(),
        get_proc_info_cached()
    )

# ⬇️ Layout geral com colunas
from rich.table import Table

def layout():
    boot_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - psutil.boot_time()))
    header = Panel(
        Text(f" {datetime.now().strftime('%H:%M:%S')}  |  Uptime: {boot_time}", style=TEXT_COLOR),
        border_style=BORDER_COLOR,
        padding=(0, 1)
    )

    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=2)

    col1 = left_column()
    col2 = right_column()

    table.add_row(col1, col2)
    return Group(header, table)

# ------------------- LOOP FINAL -------------------
if __name__ == "__main__":
    with Live(refresh_per_second=1, screen=True) as live:
        while True:
            live.update(layout())
            time.sleep(1)
