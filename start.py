#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import time
import platform
import importlib

# ────────────────────────────────────────────────────────────
# Colores (se deshabilitan automáticamente en Windows antiguo)
# ────────────────────────────────────────────────────────────
class Colors:
    _enabled = sys.stdout.isatty()

    GREEN  = '\033[92m' if _enabled else ''
    YELLOW = '\033[93m' if _enabled else ''
    RED    = '\033[91m' if _enabled else ''
    PURPLE = '\033[95m' if _enabled else ''
    BLUE   = '\033[94m' if _enabled else ''
    END    = '\033[0m'  if _enabled else ''
    BOLD   = '\033[1m'  if _enabled else ''


def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                  XONICONVER v3.3                           ║
║              Conversor Universal de Archivos               ║
║            Desarrollado por: Darian Alberto                ║
║                    Camacho Salas                           ║
║                  Organización: XONIDU                      ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)


def _pip_install(package: str):
    """Instala un paquete con pip de forma cross-platform."""
    cmd = [sys.executable, '-m', 'pip', 'install', package]
    if platform.system().lower() == 'linux':
        # En Arch/Debian/Ubuntu puede ser necesario
        cmd.append('--break-system-packages')
    subprocess.run(cmd, check=False)


def install_dependencies():
    print(f"{Colors.BOLD}Verificando dependencias...{Colors.END}")

    # (nombre_modulo, nombre_paquete_pip)
    deps = [
        ('flask',     'Flask'),
        ('PIL',       'Pillow'),
        ('pypdf',     'pypdf'),   # sucesor moderno de PyPDF2
        ('docx',      'python-docx'),
        ('qrcode',    'qrcode[pil]'),
        ('pdfplumber','pdfplumber'),
        ('waitress',  'waitress'),
    ]

    for module, package in deps:
        try:
            importlib.import_module(module)
            print(f"{Colors.GREEN}  ✔ {package}{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  ⬇  Instalando {package}...{Colors.END}")
            _pip_install(package)
            # Verificar que se instaló
            try:
                importlib.import_module(module)
                print(f"{Colors.GREEN}  ✔ {package} instalado correctamente.{Colors.END}")
            except ImportError:
                print(f"{Colors.RED}  ✘ No se pudo instalar {package}. "
                      f"Instálalo manualmente: pip install {package}{Colors.END}")

    print(f"{Colors.GREEN}Dependencias listas.{Colors.END}\n")


def is_server_alive(port: int = 5050) -> bool:
    try:
        import urllib.request
        with urllib.request.urlopen(
            f"http://localhost:{port}/health", timeout=5
        ) as resp:
            return resp.status == 200
    except Exception:
        return False


def run_server():
    port = 5050
    print(f"{Colors.BOLD}Iniciando servidor XONICONVER...{Colors.END}")
    print(f"  Servidor : waitress (multi-hilo)")
    print(f"  Puerto   : {port}")
    print(f"  Local    : http://localhost:{port}")
    print(f"  Red      : http://<tu-ip>:{port}")
    print(f"{Colors.YELLOW}  Para detener: Ctrl+C{Colors.END}")
    print("-" * 60)

    cmd = [
        sys.executable, '-m', 'waitress',
        '--host=0.0.0.0',
        f'--port={port}',
        '--threads=6',
        'xoniconver:app'
    ]

    process = None
    try:
        while True:
            if process is None or process.poll() is not None:
                print(f"{Colors.GREEN}[INFO] Lanzando servidor...{Colors.END}")
                process = subprocess.Popen(cmd)
                time.sleep(4)

            if not is_server_alive(port):
                print(f"{Colors.RED}[WARN] El servidor no responde. Reiniciando...{Colors.END}")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception:
                    process.kill()
                process = None
                time.sleep(3)
            else:
                time.sleep(10)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Deteniendo servidor...{Colors.END}")
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except Exception:
                process.kill()
        raise   # relanza para que main() capture el KeyboardInterrupt


def main():
    # Habilitar colores ANSI en Windows 10+
    if platform.system().lower() == 'windows':
        os.system('color')

    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    # Comprobar que existe el módulo principal
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xoniconver_path = os.path.join(script_dir, 'xoniconver.py')
    if not os.path.exists(xoniconver_path):
        print(f"{Colors.RED}Error: No se encuentra xoniconver.py en {script_dir}{Colors.END}")
        sys.exit(1)

    # Cambiar al directorio del script para que Flask encuentre los templates
    os.chdir(script_dir)

    install_dependencies()

    try:
        run_server()
    except KeyboardInterrupt:
        print(f"{Colors.YELLOW}¡Hasta luego!{Colors.END}")
        sys.exit(0)


if __name__ == '__main__':
    main()
