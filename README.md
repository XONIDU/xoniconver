# 📦 XONICONVER v3.2

<div align="center">
  <h3>Servicio web para conversión de archivos universal</h3>
  <p><strong>Imágenes → PDF | PDFs → PDF único | PDF → Word</strong></p>
  <p><em>#Somos XONIDU</em></p>
</div>

---

## 🎯 ¿Qué es XONICONVER?

XONICONVER es una herramienta Python que proporciona un servicio web para convertir archivos de manera sencilla y rápida. Consta de dos componentes:

- **start.py** - Lanzador universal que verifica dependencias y ejecuta el programa principal
- **xoniconver.py** - Programa principal con el servidor web y la lógica de conversión

Permite:
- 🖼️ Convertir imágenes a PDF
- 🔗 Unir múltiples PDFs en uno solo (corregido sin duplicación)
- 📝 Extraer texto de PDF a Word (.docx)

El script inicia un servidor web accesible desde cualquier dispositivo en la misma red (PC, móvil, tablet) con una interfaz responsive y moderna.

---

## 📥 Instalación

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/XONIDU/xoniconver.git
cd xoniconver
```

✅ **Requisitos**

- Python 3.6+ instalado
- Dependencias Python listadas en requisitos.txt
- Conexión a internet (solo para instalar dependencias)

### Dependencias del sistema por plataforma:

#### 🐧 Arch Linux
```bash
# Instalar dependencias del sistema
sudo pacman -Syu python-pip libjpeg-turbo zlib tk

# Instalar dependencias Python
pip install -r requisitos.txt --break-system-packages
```

#### 🐧 Ubuntu / Debian
```bash
# Actualizar repositorios
sudo apt update

# Instalar dependencias del sistema
sudo apt install python3 python3-pip python3-venv python3-tk libjpeg-dev zlib1g-dev -y

# Instalar dependencias Python
pip3 install -r requisitos.txt --break-system-packages
```

#### 🪟 Windows
```bash
# Instalar dependencias Python
pip install -r requisitos.txt
```

---

## ⚙️ Uso

### Iniciar el servidor

```bash
python start.py
```

El lanzador verificará las dependencias y automáticamente ejecutará xoniconver.py mostrando:

- ✅ Estado de las dependencias
- 🌐 URL local de acceso
- 📱 Código QR para acceso rápido desde móvil
- ✨ Características disponibles

### Acceder desde:

- **PC**: `http://localhost:5050`
- **Móvil**: `http://[TU-IP]:5050` (misma red WiFi)

### En el menú principal de XONICONVER:

```
MENU PRINCIPAL:
  1. Iniciar XONICONVER
  2. Revisar dependencias
  3. Instalar dependencias
  4. Ver README
  5. Salir
```

### Accesos directos

El lanzador crea automáticamente accesos directos para facilitar la ejecución:

- **Windows**: INICIAR_XONICONVER.bat (doble clic)
- **Linux**: INICIAR_XONICONVER.sh (ejecutar con ./INICIAR_XONICONVER.sh)
- **MacOS**: INICIAR_XONICONVER.command (doble clic)

### ✋ Detener el servidor

- Presiona `Ctrl + C` en la terminal donde se ejecuta el servidor

---

## 🎯 Funcionalidades

### 1. Imágenes a PDF
- Convierte una o múltiples imágenes en un solo archivo PDF
- Formatos soportados: PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP
- Mantiene la calidad original de las imágenes

### 2. Unir PDFs (CORREGIDO v3.2)
- **Dos métodos de unión** para máxima compatibilidad:
  - Método 1: PdfMerger (estándar)
  - Método 2: PdfWriter (alternativo)
- **Sin duplicación de páginas** - Problema solucionado en v3.2
- Combina documentos de diferentes fuentes

### 3. PDF a Word (DOCX)
- Extrae texto de archivos PDF
- Mantiene la estructura básica de títulos y párrafos
- Soporta múltiples páginas y documentos

---

## 📁 Estructura del Proyecto

```
xoniconver/
├── README.md          # Documentación
├── requisitos.txt     # Dependencias Python
├── start.py          # Lanzador universal
├── xoniconver.py     # Programa principal (servidor web)
└── templates/        # Plantillas HTML
    └── index.html    # Interfaz de usuario responsive
```

---

## 📝 Formatos Soportados

| Tipo | Formatos |
|------|----------|
| **Imágenes** | PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP |
| **Documentos** | PDF, DOCX (salida) |

---

## 🔧 Solución de Problemas

### "El puerto 5050 está en uso"
```bash
# Cambia el puerto en xoniconver.py
port = 5050  # Modificar este valor
```

### "Error de importación"
```bash
# Verifica las dependencias instaladas
pip list | grep -E "Flask|Pillow|PyPDF2|python-docx|qrcode"
```

### "Móvil no conecta"
- Verifica que ambos dispositivos estén en la misma red WiFi
- Comprueba el firewall (puerto 5050 abierto)
- Usa la IP correcta mostrada al iniciar el servidor

### "PDFs protegidos"
> ⚠️ No se pueden procesar PDFs con contraseña

### Error con `--break-system-packages`
> En sistemas que no lo requieran, omite esta bandera

### "No se encuentra xoniconver.py"
- Asegúrate de que xoniconver.py está en el mismo directorio que start.py
- Verifica la estructura del proyecto

---

## 🔒 Consideraciones de seguridad

- ✅ Procesamiento seguro en memoria (no guarda archivos en disco)
- ✅ Sin límites de tamaño en archivos
- ✅ Interfaz local (solo accesible en tu red)
- ✅ Sin almacenamiento de archivos temporales

---

## 📊 Estadísticas del proyecto

- **Versión**: 3.2
- **Lenguaje**: Python 100%
- **Última actualización**: 2026
- **Estado**: Stable

---

## ✉️ Contacto y Créditos

- **Proyecto**: XONICONVER
- **Email**: xonidu@gmail.com
- **Instagram**: @xonidu
- **Facebook**: xonidu
- **Creador**: Darian Alberto Camacho Salas
- **#Somos XONIDU**

---
