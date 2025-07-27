import os
import sys
import random
import shutil
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(BASE_DIR, "venv")
PYTHON_EXEC = os.path.join(VENV_PATH, "Scripts" if os.name == "nt" else "bin", "python")
CONFIG_FILE = os.path.join(BASE_DIR, "config_color.txt")

# Agora imports após garantir venv
import colorama
from colorama import init, Fore

init(autoreset=True)

CORES = {
    "verde": Fore.GREEN,
    "vermelho": Fore.RED,
    "azul": Fore.BLUE,
    "amarelo": Fore.YELLOW,
    "ciano": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "branco": Fore.WHITE,
}

def salvar_cor(cor_str):
    with open(CONFIG_FILE, "w") as f:
        f.write(cor_str)

def carregar_cor():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cor = f.read().strip().lower()
            if cor in CORES:
                return cor
    return None

def main():
    os.system("cls" if os.name == "nt" else "clear")

    cor_salva = carregar_cor()
    if cor_salva:
        print(f"Cor carregada das configurações: {cor_salva}")
        cor_input = cor_salva
    else:
        print("Cores disponíveis: " + ", ".join(CORES.keys()))
        cor_input = input("Digite a cor desejada (ou pressione Enter para verde): ").strip().lower()
        if not cor_input:
            cor_input = "verde"
        salvar_cor(cor_input)

    COR = CORES.get(cor_input, Fore.GREEN)

    largura, altura = shutil.get_terminal_size()
    quedas = [0] * largura

    try:
        while True:
            print("\033[1;40m", end="")
            for i in range(largura):
                if random.random() > 0.975:
                    print(COR + chr(random.randint(33, 126)), end="")
                    quedas[i] = 0
                elif quedas[i] < altura:
                    print(" ", end="")
                    quedas[i] += 1
                else:
                    quedas[i] = 0
                    print(" ", end="")
            print()
            time.sleep(0.05)
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()
