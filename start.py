#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICONVER v3.2 - Conversor Universal de Archivos - Installer/Launcher
Este script ejecuta xoniconver.py y verifica/instala dependencias
con múltiples estrategias de fallback para todas las plataformas.
Desarrollado por: Darian Alberto Camacho Salas
#Somos XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util
import time
import socket
import webbrowser

# ============================================================================
# Colores para terminal
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Detección del sistema
# ============================================================================
def get_system():
    return platform.system().lower()

def get_linux_distro():
    if get_system() != 'linux':
        return None
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content or 'mint' in content:
                    return 'debian-based'
                elif 'arch' in content or 'manjaro' in content:
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'opensuse' in content:
                    return 'opensuse'
                elif 'centos' in content or 'rhel' in content:
                    return 'rhel-based'
        if shutil.which('apt'):
            return 'debian-based'
        elif shutil.which('pacman'):
            return 'arch-based'
        elif shutil.which('dnf'):
            return 'fedora'
        elif shutil.which('zypper'):
            return 'opensuse'
        elif shutil.which('yum'):
            return 'rhel-based'
        return 'linux-generic'
    except:
        return 'linux-generic'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    else:
        for cmd in ['python3', 'python']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                return [cmd]
            except:
                continue
        return ['python3']

def get_pip_commands():
    """Retorna múltiples comandos pip posibles en orden de preferencia"""
    cmds = []
    python_cmd = get_python_command()[0]
    
    cmds.append([sys.executable, '-m', 'pip'])
    if shutil.which('pip3'):
        cmds.append(['pip3'])
    if shutil.which('pip'):
        cmds.append(['pip'])
    if python_cmd != sys.executable:
        cmds.append([python_cmd, '-m', 'pip'])
    
    return cmds

def get_install_strategies(packages):
    """Genera múltiples estrategias de instalación para fallback"""
    strategies = []
    system = get_system()
    distro = get_linux_distro()
    
    strategies.append(['--break-system-packages'])
    strategies.append(['--user'])
    strategies.append([])
    strategies.append(['--ignore-installed'])
    strategies.append(['--no-deps'])
    
    if system == 'linux':
        if distro in ['debian-based']:
            strategies.insert(1, ['--system'])
        elif distro in ['arch-based', 'fedora']:
            strategies.insert(0, ['--break-system-packages'])
    elif system == 'darwin':
        strategies.append(['--user'])
    elif system == 'windows':
        strategies.append(['--no-warn-script-location'])
    
    return strategies

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_xoniconver_path():
    script_dir = get_script_dir()
    rutas = [
        os.path.join(script_dir, 'xoniconver.py'),
        os.path.join(os.getcwd(), 'xoniconver.py')
    ]
    for r in rutas:
        if os.path.exists(r):
            return r
    return None

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "127.0.0.1"

def check_port(port=5050):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

# ============================================================================
# Funciones de banner y ayuda
# ============================================================================
def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'UNKNOWN')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                 XONICONVER v3.2 - CORREGIDO               
              Conversor Universal de Archivos              
              Imagenes -> PDF | Unir PDFs | PDF -> Word   
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
              #Somos XONIDU
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}USO DE XONICONVER:{Colors.END}

  python start.py [opciones]

{Colors.BOLD}DESCRIPCION:{Colors.END}

  XONICONVER es un servicio web para convertir archivos de forma universal.
  Inicia un servidor web accesible desde PC o movil en la misma red.

{Colors.BOLD}OPCIONES:{Colors.END}

  --help, -h        Muestra esta ayuda
  --no-install      Salta la verificacion/instalacion de dependencias
  --port N          Usa el puerto N en lugar del 5050 por defecto
  --no-browser      No abre el navegador automaticamente
  --waitress        Usa Waitress en lugar del servidor de desarrollo de Flask

{Colors.BOLD}EJEMPLOS:{Colors.END}

  Inicio normal:
    python start.py

  Inicio con puerto personalizado:
    python start.py --port 8080

  Saltar instalacion de dependencias:
    python start.py --no-install

  Usar Waitress (recomendado para produccion):
    python start.py --waitress
    """
    print(ayuda)

# ============================================================================
# Verificación de dependencias
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    for pip_cmd in get_pip_commands():
        try:
            subprocess.run(pip_cmd + ['--version'], capture_output=True, check=True)
            return True, pip_cmd
        except:
            continue
    return False, None

def install_pip_linux():
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    
    instaladores = []
    if distro == 'debian-based':
        instaladores = [
            ['sudo', 'apt', 'update'],
            ['sudo', 'apt', 'install', '-y', 'python3-pip']
        ]
    elif distro == 'arch-based':
        instaladores = [
            ['sudo', 'pacman', '-S', '--noconfirm', 'python-pip']
        ]
    elif distro == 'fedora':
        instaladores = [
            ['sudo', 'dnf', 'install', '-y', 'python3-pip']
        ]
    elif distro == 'opensuse':
        instaladores = [
            ['sudo', 'zypper', 'refresh'],
            ['sudo', 'zypper', 'install', '-y', 'python3-pip']
        ]
    elif distro == 'rhel-based':
        instaladores = [
            ['sudo', 'yum', 'install', '-y', 'python3-pip']
        ]
    else:
        instaladores = [
            [sys.executable, '-m', 'ensurepip', '--upgrade']
        ]
    
    for cmd in instaladores:
        try:
            subprocess.run(cmd, check=True)
            return True
        except:
            continue
    return False

def install_pip_windows():
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        try:
            import urllib.request
            urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
            subprocess.run([sys.executable, 'get-pip.py'], check=True)
            os.remove('get-pip.py')
            return True
        except:
            return False

def check_python_module(module_name):
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    print(f"\n{Colors.BOLD}Verificando dependencias...{Colors.END}")
    
    dependencies = [
        ('flask', 'Flask', 'Framework web'),
        ('PIL', 'Pillow', 'Procesamiento de imagenes'),
        ('PyPDF2', 'PyPDF2', 'Manipulacion de PDFs'),
        ('docx', 'python-docx', 'Generacion de Word'),
        ('qrcode', 'qrcode', 'Generacion de QR'),
        ('werkzeug', 'Werkzeug', 'Utilidades WSGI'),
    ]
    
    missing = []
    for module, package, desc in dependencies:
        import_name = module
        if module == 'PIL':
            import_name = 'PIL'
        try:
            __import__(import_name)
            print(f"{Colors.GREEN}  - {package} ({desc}): OK{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  - {package} ({desc}): FALTANTE{Colors.END}")
            missing.append(package)
    
    # Verificar waitress opcional
    try:
        __import__('waitress')
        print(f"{Colors.GREEN}  - waitress (servidor produccion): OK{Colors.END}")
    except ImportError:
        print(f"{Colors.YELLOW}  - waitress (servidor produccion): OPCIONAL{Colors.END}")
        # No lo agregamos a missing, es opcional
    
    return missing

def install_with_pip(packages):
    if not packages:
        return True
    
    pip_ok, pip_cmd = check_pip()
    if not pip_ok:
        print(f"{Colors.RED}No se encontro pip. Intentando instalar...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip automaticamente{Colors.END}")
                return False
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip automaticamente{Colors.END}")
                return False
        pip_ok, pip_cmd = check_pip()
        if not pip_ok:
            return False
    
    strategies = get_install_strategies(packages)
    pip_base = pip_cmd if pip_cmd else ['pip']
    
    for flags in strategies:
        cmd = pip_base + ['install'] + flags + packages
        flag_desc = ' '.join(flags) if flags else '(sin flags)'
        print(f"\n  Intentando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"{Colors.GREEN}  Exito con {flag_desc}{Colors.END}")
                return True
            else:
                error_msg = result.stderr[:200] if result.stderr else result.stdout[:200]
                print(f"{Colors.YELLOW}  Fallo: {error_msg}{Colors.END}")
        except subprocess.TimeoutExpired:
            print(f"{Colors.YELLOW}  Timeout{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}  Error: {str(e)[:100]}{Colors.END}")
    
    print(f"{Colors.RED}No se pudieron instalar las dependencias automaticamente{Colors.END}")
    return False

def verify_imports():
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    modules = [
        ('flask', 'Flask'),
        ('PIL', 'Pillow'),
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('qrcode', 'qrcode'),
        ('werkzeug', 'Werkzeug'),
    ]
    all_ok = True
    for module, name in modules:
        try:
            __import__(module)
            print(f"{Colors.GREEN}  - {name}: OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}  - {name}: FALLO{Colors.END}")
            all_ok = False
    return all_ok

# ============================================================================
# Creación de accesos directos
# ============================================================================
def create_shortcuts():
    system = get_system()
    
    if system == 'windows':
        with open('INICIAR_XONICONVER.bat', 'w') as f:
            f.write("""@echo off
title XONICONVER v3.2 - Conversor Universal
color 0A
echo ========================================
echo      XONICONVER v3.2 - Conversor Universal
echo      Desarrollado por Darian Alberto Camacho Salas
echo      #Somos XONIDU
echo ========================================
echo.
python start.py
pause
""")
        print(f"{Colors.GREEN}Creado INICIAR_XONICONVER.bat{Colors.END}")
    elif system == 'linux':
        with open('INICIAR_XONICONVER.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONICONVER v3.2 - Conversor Universal"
echo "      Desarrollado por Darian Alberto Camacho Salas"
echo "      #Somos XONIDU"
echo "========================================"
echo ""
python3 start.py
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONICONVER.sh', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONICONVER.sh{Colors.END}")
    elif system == 'darwin':
        with open('INICIAR_XONICONVER.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONICONVER v3.2 - Conversor Universal"
echo "      Desarrollado por Darian Alberto Camacho Salas"
echo "      #Somos XONIDU"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONICONVER.command', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONICONVER.command{Colors.END}")

# ============================================================================
# Función principal de lanzamiento
# ============================================================================
def launch_server(use_waitress=False, port=5050, open_browser=True):
    xoniconver_path = get_xoniconver_path()
    if not xoniconver_path:
        print(f"{Colors.RED}Error: No se encuentra xoniconver.py{Colors.END}")
        return False
    
    # Verificar puerto
    if not check_port(port):
        print(f"{Colors.YELLOW}El puerto {port} esta en uso{Colors.END}")
        respuesta = input(f"Intentar de todas formas? (s/n): ")
        if respuesta.lower() != 's':
            return False
    
    # Mostrar información de acceso
    local_ip = get_local_ip()
    print(f"\n{Colors.BOLD}Servidor listo para iniciar{Colors.END}")
    print(f"  Local:   {Colors.BOLD}http://localhost:{port}{Colors.END}")
    print(f"  Red:     {Colors.BOLD}http://{local_ip}:{port}{Colors.END}")
    print(f"  Puerto:  {port}")
    print(f"{Colors.YELLOW}Presiona Ctrl+C para detener el servidor{Colors.END}")
    
    if open_browser:
        try:
            webbrowser.open(f"http://localhost:{port}")
        except:
            pass
    
    # Elegir método de ejecución
    if use_waitress:
        # Verificar que waitress esté instalado
        try:
            import waitress
            print(f"{Colors.CYAN}Usando Waitress (servidor de produccion){Colors.END}")
            cmd = [sys.executable, '-m', 'waitress', '--host=0.0.0.0', f'--port={port}', '--threads=6', 'xoniconver:app']
        except ImportError:
            print(f"{Colors.YELLOW}Waitress no instalado, usando Flask development server{Colors.END}")
            cmd = [sys.executable, xoniconver_path]
            # Pasar argumentos de puerto a la aplicación
            os.environ['XONICONVER_PORT'] = str(port)
    else:
        cmd = [sys.executable, xoniconver_path]
        os.environ['XONICONVER_PORT'] = str(port)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Servidor detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error al ejecutar: {e}{Colors.END}")
        return False
    return True

# ============================================================================
# Menú interactivo
# ============================================================================
def show_menu():
    print(f"\n{Colors.BOLD}MENU PRINCIPAL:{Colors.END}")
    print(f"{Colors.BLUE}1.{Colors.END} Iniciar XONICONVER (con Flask development server)")
    print(f"{Colors.BLUE}2.{Colors.END} Iniciar XONICONVER (con Waitress - produccion)")
    print(f"{Colors.BLUE}3.{Colors.END} Revisar dependencias")
    print(f"{Colors.BLUE}4.{Colors.END} Instalar dependencias")
    print(f"{Colors.BLUE}5.{Colors.END} Ver README")
    print(f"{Colors.BLUE}6.{Colors.END} Salir")
    
    choice = input(f"\n{Colors.BOLD}Selecciona una opcion (1-6): {Colors.END}")
    return choice

def show_readme():
    readme_path = os.path.join(get_script_dir(), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
            print(f.read())
            print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}README.md no encontrado{Colors.END}")
    input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.END}")

# ============================================================================
# Función main
# ============================================================================
def main():
    # Parsear argumentos
    no_install = False
    use_waitress = False
    port = 5050
    open_browser = True
    show_help = False
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ['--help', '-h']:
            show_help = True
        elif arg == '--no-install':
            no_install = True
        elif arg == '--waitress':
            use_waitress = True
        elif arg == '--no-browser':
            open_browser = False
        elif arg == '--port':
            if i+1 < len(sys.argv):
                try:
                    port = int(sys.argv[i+1])
                    i += 1
                except:
                    print(f"{Colors.RED}Puerto invalido{Colors.END}")
                    return
            else:
                print(f"{Colors.RED}Falta el puerto para --port{Colors.END}")
                return
        i += 1
    
    if show_help:
        print_banner()
        mostrar_ayuda()
        return
    
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    print_banner()
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado{Colors.END}")
        print("Descarga desde: https://www.python.org/downloads/")
        sys.exit(1)
    
    python_version = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    
    # Verificar/instalar pip
    pip_ok, _ = check_pip()
    if not pip_ok:
        print(f"\n{Colors.YELLOW}Pip no encontrado. Instalando...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip automaticamente{Colors.END}")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip automaticamente{Colors.END}")
                sys.exit(1)
    
    # Instalar dependencias si no se salta
    if not no_install:
        missing = check_dependencies()
        if missing:
            print(f"\n{Colors.YELLOW}Faltan {len(missing)} dependencias: {', '.join(missing)}{Colors.END}")
            respuesta = input("Instalar automaticamente? (s/n): ")
            if respuesta.lower() == 's':
                if install_with_pip(missing):
                    print(f"{Colors.GREEN}Dependencias instaladas correctamente{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}Instalacion automatica fallida. Puedes instalar manualmente:{Colors.END}")
                    print(f"  pip install {' '.join(missing)}")
                    if get_system() == 'linux':
                        print("  O con: pip install --break-system-packages " + ' '.join(missing))
            else:
                print(f"{Colors.YELLOW}Continuando sin algunas dependencias...{Colors.END}")
        
        # Verificar importaciones
        verify_imports()
    
    # Crear accesos directos
    create_shortcuts()
    
    # Si se pasaron argumentos para iniciar directamente, hacerlo sin menú
    if len(sys.argv) > 1 and any(a in sys.argv for a in ['--port', '--waitress', '--no-install', '--no-browser']):
        launch_server(use_waitress, port, open_browser)
        return
    
    # Menú interactivo
    while True:
        choice = show_menu()
        if choice == '1':
            launch_server(use_waitress=False, port=port, open_browser=True)
        elif choice == '2':
            # Asegurar que waitress esté instalado
            try:
                import waitress
            except ImportError:
                print(f"{Colors.YELLOW}Waitress no instalado, instalando...{Colors.END}")
                install_with_pip(['waitress'])
            launch_server(use_waitress=True, port=port, open_browser=True)
        elif choice == '3':
            check_dependencies()
            verify_imports()
            input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.END}")
        elif choice == '4':
            missing = check_dependencies()
            if missing:
                install_with_pip(missing)
            else:
                print(f"{Colors.GREEN}No hay dependencias faltantes{Colors.END}")
            input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.END}")
        elif choice == '5':
            show_readme()
        elif choice == '6':
            print(f"\n{Colors.GREEN}Gracias por usar XONICONVER{Colors.END}")
            print(f"{Colors.GREEN}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
            print(f"{Colors.GREEN}#Somos XONIDU{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Opcion no valida{Colors.END}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")