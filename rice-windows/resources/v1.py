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

# Funções de mensagem
def print_ok(msg):
    print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} {msg}")

def print_info(msg):
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} {msg}")

def print_fail(msg):
    print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} {msg}")

# Função de download
def baixar_arquivo(url, destino):
    try:
        print_info(f"Baixando: {url}")
        r = requests.get(url)
        r.raise_for_status()
        with open(destino, "w", encoding="utf-8") as f:
            f.write(r.text)
        print_ok(f"Salvo em: {destino}")
    except Exception as e:
        print_fail(f"Erro ao baixar {url}: {e}")
        sys.exit(1)

# Principal
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
        time.sleep(1)

    print_ok("Todos os arquivos foram baixados com sucesso.")

if __name__ == "__main__":
    main()
