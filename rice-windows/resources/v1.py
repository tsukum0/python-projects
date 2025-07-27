import os
import time

# Códigos ANSI para cores
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

def print_ok(msg):
    print(f"{GREEN}[OK]{RESET} {msg}")

def print_info(msg):
    print(f"{YELLOW}[INFO]{RESET} {msg}")

def print_fail(msg):
    print(f"{RED}[FAIL]{RESET} {msg}")

def remover_temporarios():
    base = os.path.dirname(os.path.abspath(__file__))
    temp_path = os.path.join(base, "temporarios.txt")

    if os.path.exists(temp_path):
        with open(temp_path, "r") as f:
            arquivos = [linha.strip() for linha in f if linha.strip()]
        for arquivo in arquivos:
            alvo = os.path.join(base, arquivo)
            if os.path.exists(alvo):
                try:
                    os.remove(alvo)
                    print_ok(f"Removido: {arquivo}")
                except Exception as e:
                    print_fail(f"Falha ao remover {arquivo}: {e}")
        try:
            os.remove(temp_path)
        except:
            pass

def main():
    print_info("Instalador simulado iniciado...")
    time.sleep(2)
    print_ok("Simulacao completa.")
    time.sleep(1)
    remover_temporarios()

if __name__ == "__main__":
    main()
