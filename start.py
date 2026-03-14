#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICONVER v3.2 - Instalador y Ejecutor
#Somos XONIDU
"""

import os
import sys
import subprocess
import platform
import time
import importlib.util

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Muestra el banner de XONICONVER"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}XONICONVER v3.2 - Instalador y Ejecutor{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}Herramienta: Instalacion automatica y ejecucion{Colors.END}")
    print(f"{Colors.GREEN}Creador: Darian Alberto Camacho Salas{Colors.END}")
    print(f"{Colors.GREEN}#Somos XONIDU{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def check_python_version():
    """Verifica la version de Python"""
    print(f"{Colors.BLUE}Verificando version de Python...{Colors.END}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"{Colors.GREEN}Python {version.major}.{version.minor}.{version.micro} OK{Colors.END}")
        return True
    else:
        print(f"{Colors.FAIL}Se requiere Python 3.6 o superior{Colors.END}")
        return False

def check_dependencies():
    """Verifica que dependencias estan instaladas"""
    dependencies = ['flask', 'PIL', 'PyPDF2', 'docx', 'qrcode']
    missing = []
    installed = []
    
    print(f"{Colors.BLUE}Verificando dependencias...{Colors.END}")
    
    for dep in dependencies:
        spec = importlib.util.find_spec(dep)
        if spec is None:
            missing.append(dep)
        else:
            installed.append(dep)
    
    if installed:
        print(f"{Colors.GREEN}Instaladas: {', '.join(installed)}{Colors.END}")
    if missing:
        print(f"{Colors.WARNING}Faltantes: {', '.join(missing)}{Colors.END}")
    
    return missing

def install_dependencies():
    """Instala las dependencias faltantes"""
    system = platform.system().lower()
    missing = check_dependencies()
    
    if not missing:
        print(f"{Colors.GREEN}Todas las dependencias estan instaladas{Colors.END}")
        return True
    
    print(f"\n{Colors.BLUE}Instalando dependencias faltantes...{Colors.END}")
    
    pip_cmd = [sys.executable, '-m', 'pip', 'install']
    packages = ['Flask', 'Pillow', 'PyPDF2', 'python-docx', 'qrcode']
    
    if system == 'linux':
        pip_cmd.append('--break-system-packages')
    
    try:
        for package in packages:
            print(f"{Colors.BLUE}   Instalando {package}...{Colors.END}")
            subprocess.check_call(pip_cmd + [package], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        print(f"{Colors.GREEN}Todas las dependencias instaladas correctamente{Colors.END}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}Error instalando dependencias: {e}{Colors.END}")
        return False

def check_system_dependencies():
    """Verifica dependencias del sistema (Linux)"""
    if platform.system().lower() != 'linux':
        return True
    
    print(f"{Colors.BLUE}Verificando dependencias del sistema...{Colors.END}")
    
    if os.path.exists('/etc/arch-release'):
        pkgs = ['python-pip', 'libjpeg-turbo', 'zlib', 'tk']
        cmd = ['pacman', '-Q'] + pkgs
    elif os.path.exists('/etc/debian_version'):
        pkgs = ['python3', 'python3-pip', 'python3-venv', 'python3-tk', 'libjpeg-dev', 'zlib1g-dev']
        cmd = ['dpkg', '-l'] + pkgs
    else:
        return True
    
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"{Colors.GREEN}Dependencias del sistema OK{Colors.END}")
        return True
    except:
        print(f"{Colors.WARNING}Algunas dependencias del sistema podrian faltar{Colors.END}")
        print(f"{Colors.WARNING}Revisa el README.md para instalarlas manualmente{Colors.END}")
        return True

def check_port(port=5050):
    """Verifica si el puerto esta disponible"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def get_local_ip():
    """Obtiene la IP local"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "127.0.0.1"

def show_menu():
    """Muestra el menu principal"""
    print(f"\n{Colors.BOLD}MENU PRINCIPAL:{Colors.END}")
    print(f"{Colors.BLUE}1.{Colors.END} Iniciar XONICONVER")
    print(f"{Colors.BLUE}2.{Colors.END} Revisar dependencias")
    print(f"{Colors.BLUE}3.{Colors.END} Instalar dependencias")
    print(f"{Colors.BLUE}4.{Colors.END} Ver README")
    print(f"{Colors.BLUE}5.{Colors.END} Salir")
    
    choice = input(f"\n{Colors.BOLD}Selecciona una opcion (1-5): {Colors.END}")
    return choice

def show_readme():
    """Muestra el README"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
            print(f.read())
            print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    else:
        print(f"{Colors.WARNING}Archivo README.md no encontrado{Colors.END}")
    
    input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.END}")

def start_xoniconver():
    """Inicia XONICONVER"""
    if not check_port():
        print(f"{Colors.WARNING}El puerto 5050 esta en uso{Colors.END}")
        response = input(f"{Colors.BOLD}Intentar de todas formas? (s/n): {Colors.END}")
        if response.lower() != 's':
            return
    
    main_file = os.path.join(os.path.dirname(__file__), 'xoniconver.py')
    if not os.path.exists(main_file):
        print(f"{Colors.FAIL}No se encuentra xoniconver.py{Colors.END}")
        return
    
    print(f"\n{Colors.GREEN}Todo listo para iniciar{Colors.END}")
    print(f"{Colors.BLUE}Servidor disponible en:{Colors.END}")
    print(f"   Local: {Colors.BOLD}http://localhost:5050{Colors.END}")
    print(f"   Red:   {Colors.BOLD}http://{get_local_ip()}:5050{Colors.END}")
    print(f"\n{Colors.WARNING}Presiona Ctrl+C para detener el servidor{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    time.sleep(2)
    
    try:
        subprocess.run([sys.executable, main_file])
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Servidor detenido{Colors.END}")
    except Exception as e:
        print(f"{Colors.FAIL}Error al ejecutar: {e}{Colors.END}")

def main():
    """Funcion principal"""
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    check_system_dependencies()
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            if not check_dependencies():
                print(f"{Colors.WARNING}Faltan dependencias{Colors.END}")
                response = input(f"{Colors.BOLD}Instalar ahora? (s/n): {Colors.END}")
                if response.lower() == 's':
                    if install_dependencies():
                        start_xoniconver()
                else:
                    print(f"{Colors.WARNING}No se puede iniciar sin dependencias{Colors.END}")
            else:
                start_xoniconver()
        
        elif choice == '2':
            check_dependencies()
            input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.END}")
        
        elif choice == '3':
            install_dependencies()
            input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.END}")
        
        elif choice == '4':
            show_readme()
        
        elif choice == '5':
            print(f"\n{Colors.GREEN}Hasta luego! #SomosXONIDU{Colors.END}")
            sys.exit(0)
        
        else:
            print(f"{Colors.FAIL}Opcion no valida{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}Hasta luego!{Colors.END}")
        sys.exit(0)
