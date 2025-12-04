# XONI-CONVER

Pequeño servicio web para convertir archivos: imágenes → PDF, unir PDFs y extraer texto de PDF → Word (.docx).
Interfaz responsive pensada para uso desde móviles y escritorio. Escucha por defecto en 0.0.0.0:5050.

---

## Requisitos (resumen)

- Python 3.8+
- Paquetes Python (ver `requirements.txt`):
  - Flask
  - Pillow
  - PyPDF2
  - python-docx

Se recomienda instalar dentro de un virtualenv para evitar tocar paquetes del sistema.

---

## Instalación y dependencias por plataforma

### Recomendado: crear y activar virtualenv (igual en todas las plataformas)
```bash
python3 -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Windows (CMD)
.\venv\Scripts\activate.bat

pip install -r requirements.txt
```

### Arch Linux
Dependencias del sistema (para Pillow y herramientas):
```bash
sudo pacman -Syu
sudo pacman -S python-pip libjpeg-turbo zlib tk
```
Si no usas virtualenv y necesitas forzar la instalación con pip del sistema:
```bash
pip install -r requirements.txt --break-system-packages
```

### Ubuntu / Debian y derivados
Dependencias del sistema:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk libjpeg-dev zlib1g-dev
```
Instalar paquetes Python:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
(Opcional, sin venv):
```bash
pip3 install -r requirements.txt --break-system-packages
```

### Fedora
```bash
sudo dnf update
sudo dnf install -y python3 python3-pip python3-virtualenv tkinter libjpeg-turbo-devel zlib-devel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
1. Instala Python 3 desde https://python.org si no lo tienes.
2. Crear y activar virtualenv (PowerShell/CMD) y luego:
```powershell
pip install -r requirements.txt
```
En Windows normalmente no necesitas `--break-system-packages`.

---

## Ejecutar la aplicación (desarrollo)

Desde la raíz del proyecto y con el virtualenv activado:
```bash
python page.py
```
Por defecto la app arranca en:
http://0.0.0.0:5050

Si la ejecutas en tu equipo, conéctate desde el móvil al IP del host (por ejemplo http://192.168.1.10:5050).

---
En Windows puedes usar waitress:
```bash
pip install waitress
waitress-serve --listen=0.0.0.0:5050 page:app
```

Si vas a exponer el servicio a Internet, usa un proxy inverso (nginx) con TLS y limita el tamaño máximo de subida a tu requerimiento.

---

## Uso

1. Abre la página en el navegador del móvil o PC: http://<IP_DEL_HOST>:5050
2. Selecciona la conversión:
   - Imágenes → PDF
   - Unir varios PDFs → PDF único
   - PDF → Word (.docx) (extrae texto)
3. Selecciona los archivos y pulsa "Convertir". La respuesta será una descarga del archivo resultante (PDF, DOCX o ZIP).

## Depuración

- Revisa la consola donde se ejecuta `python page.py` para ver errores y la IP en la que está escuchando.
- Si ves errores relacionados con Pillow en Linux, instala las librerías del sistema (libjpeg, zlib, freetype).

---

## Licencia y contacto

Proyecto: XONI-CONVER
Contacto: xonidu@gmail.com

--- 
