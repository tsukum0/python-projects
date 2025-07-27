import os
import sys
import time

try:
    import requests
    from colorama import init, Fore, Style
except ImportError:
    print("[FAIL] Bibliotecas 'requests' ou 'colorama' nao estao instaladas.")
    print("Instale com: pip install requests colorama")
    sys.exit(1)

init(autoreset=True)

def print_ok(msg):
    print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} {msg}")

def print_info(msg):
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} {msg}")

def print_fail(msg):
    print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} {msg}")

def baixar_para(nome_arquivo, url):
    try:
        print_info(f"Baixando {nome_arquivo} de:\n  {url}")
        r = requests.get(url)
        r.raise_for_status()
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(r.text)
        print_ok(f"{nome_arquivo} salvo com sucesso.")
    except Exception as e:
        print_fail(f"Erro ao baixar {nome_arquivo}: {e}")
        sys.exit(1)

def criar_iniciar_bat(nomes_arquivos):
    with open("iniciar.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("chcp 65001 >nul\n")
        for nome in nomes_arquivos:
            f.write(f"start python {nome}\n")
        f.write("exit\n")
    print_ok("Arquivo iniciar.bat criado.")

def remover_este_arquivo():
    try:
        caminho = os.path.abspath(__file__)
        os.remove(caminho)
        print_ok("instalador.py removido com sucesso.")
    except Exception as e:
        print_fail(f"Erro ao remover instalador.py: {e}")

def main():
    arquivos = {
        "programa1.py": "https://raw.githubusercontent.com/seu_usuario/seu_repo/main/programa1.py",
        "programa2.py": "https://raw.githubusercontent.com/seu_usuario/seu_repo/main/programa2.py",
        "programa3.py": "https://raw.githubusercontent.com/seu_usuario/seu_repo/main/programa3.py",
    }

    for nome, url in arquivos.items():
        baixar_para(nome, url)
        time.sleep(1)

    criar_iniciar_bat(list(arquivos.keys()))

    print_info("Finalizando instalador...")
    time.sleep(1)
    remover_este_arquivo()

if __name__ == "__main__":
    main()
