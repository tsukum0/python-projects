import os
import sys
import time

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

def baixar_arquivo(url, destino):
    try:
        import requests
    except ImportError:
        print_fail("Modulo 'requests' nao encontrado. Instale com: pip install requests")
        sys.exit(1)

    try:
        print_info(f"Baixando {url} ...")
        r = requests.get(url)
        r.raise_for_status()
        with open(destino, "w", encoding="utf-8") as f:
            f.write(r.text)
        print_ok(f"Arquivo salvo: {destino}")
    except Exception as e:
        print_fail(f"Erro ao baixar {url}: {e}")
        sys.exit(1)

def main():
    projeto_dir = "meu_projeto"
    if not os.path.exists(projeto_dir):
        os.makedirs(projeto_dir)
        print_ok(f"Pasta criada: {projeto_dir}")
    else:
        print_info(f"Pasta ja existe: {projeto_dir}")

    arquivos = {
        "programa1.py": "https://raw.githubusercontent.com/seu_usuario/seu_repo/main/programa1.py",
        "programa2.py": "https://raw.githubusercontent.com/seu_usuario/seu_repo/main/programa2.py",
        "programa3.py": "https://raw.githubusercontent.com/seu_usuario/seu_repo/main/programa3.py",
    }

    for nome_arquivo, url in arquivos.items():
        destino = os.path.join(projeto_dir, nome_arquivo)
        baixar_arquivo(url, destino)
        time.sleep(1)  # delay só pra mostrar progresso legal

    print_ok("Todos os programas foram baixados e salvos.")

if __name__ == "__main__":
    main()
