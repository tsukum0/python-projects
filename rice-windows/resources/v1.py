import os
import time

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
                    print(f"[✓] Removido: {arquivo}")
                except Exception as e:
                    print(f"[x] Falha ao remover {arquivo}: {e}")
        try:
            os.remove(temp_path)
        except:
            pass

def main():
    print("[*] Instalador simulado iniciado...")
    time.sleep(2)
    print("[✓] Simulação completa.")
    time.sleep(1)
    remover_temporarios()

if __name__ == "__main__":
    main()

