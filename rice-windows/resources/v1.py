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

def baixar_para(destino, url):
    try:
        print_info(f"Baixando:\n  {url}")
        r = requests.get(url)
        r.raise_for_status()
        with open(destino, "w", encoding="utf-8") as f:
            f.write(r.text)
        print_ok(f"Salvo em: {destino}")
    except Exception as e:
        print_fail(f"Erro ao baixar para {destino}: {e}")
        sys.exit(1)

def criar_iniciar_bat(dir_base, nomes_arquivos):
    caminho_bat = os.path.join(dir_base, "iniciar.bat")
    with open(caminho_bat, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("chcp 65001 >nul\n")
        for i, nome in enumerate(nomes_arquivos):
            f.write(f"start cmd /k python {nome}\n")
            if i < len(nomes_arquivos) - 1:
                f.write("timeout /t 5 /nobreak >nul\n")

def remover_este_arquivo():
    try:
        caminho = os.path.abspath(__file__)
        os.remove(caminho)
        print_ok("instalador.py removido com sucesso.")
    except Exception as e:
        print_fail(f"Erro ao remover instalador.py: {e}")

def main():
    pasta_destino = "windows_ricer"

    if not os.path.exists(pasta_destino):
        print_fail(f"Pasta '{pasta_destino}' nao encontrada.")
        sys.exit(1)

    arquivos = {
        "code_rain.py": "https://raw.githubusercontent.com/tsukum0/python-projects/refs/heads/main/rice-windows/programs/code_rain.py",
        "rsc_manager.py": "https://raw.githubusercontent.com/tsukum0/python-projects/refs/heads/main/rice-windows/programs/rsc_manager.py",
        "win_nfetch.py": "https://raw.githubusercontent.com/tsukum0/python-projects/refs/heads/main/rice-windows/programs/win_nfetch.py",
    }

    # Baixar arquivos principais
    for nome, url in arquivos.items():
        destino = os.path.join(pasta_destino, nome)
        baixar_para(destino, url)
        time.sleep(1)

    # Baixar requirements.txt
    req_url = "https://raw.githubusercontent.com/tsukum0/python-projects/refs/heads/main/rice-windows/resources/rq.txt"
    req_destino = os.path.join(pasta_destino, "requirements.txt")
    baixar_para(req_destino, req_url)

    criar_iniciar_bat(pasta_destino, list(arquivos.keys()))

    print_info("Finalizando instalador...")
    time.sleep(1)
    remover_este_arquivo()

if __name__ == "__main__":
    main()
