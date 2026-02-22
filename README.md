# 📦 XONICONVER v3.2

<div align="center">
  <h3>Servicio web para conversión de archivos universal</h3>
  <p><strong>Imágenes → PDF | PDFs → PDF único | PDF → Word</strong></p>
  <p><em>#Somos XONIDU</em></p>
</div>

---

## ✨ Características Principales

- 🖼️ **Conversión de Imágenes a PDF** - Convierte múltiples imágenes en un solo PDF
- 🔗 **Unión de PDFs** - Combina múltiples PDFs en uno solo (corregido sin duplicación)
- 📝 **Extracción de Texto** - Convierte PDF a Word (.docx) extrayendo texto
- 📱 **Interfaz Responsive** - Diseño adaptable para PC y dispositivos móviles
- 🔒 **Procesamiento Seguro** - Todo el procesamiento se realiza en memoria
- ⚡ **Sin Límites de Tamaño** - Procesa archivos de cualquier tamaño
- 🎨 **Diseño Moderno** - Interfaz elegante con drag & drop
- 📤 **Múltiples Formatos** - Soporte para PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP y PDF

---

## 🚀 Instalación Rápida

### 🐧 Arch Linux
```bash
sudo pacman -Syu python-pip libjpeg-turbo zlib tk
pip install Flask Pillow PyPDF2 python-docx qrcode --break-system-packages
```

### 🐧 Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk libjpeg-dev zlib1g-dev
pip3 install Flask Pillow PyPDF2 python-docx qrcode --break-system-packages
```

### 🪟 Windows
```bash
pip install Flask Pillow PyPDF2 python-docx qrcode
```

---

## 📦 Estructura del Proyecto

```
xoniconver/
├── README.md          # Documentación
├── requisitos.txt     # Dependencias del proyecto
├── start.py          # Código principal (Python)
└── templates/        # Plantillas HTML
    └── index.html    # Interfaz de usuario
```

---

## 🎯 Uso

### Iniciar el Servidor
```bash
python start.py
```

### Acceder desde:
- **PC**: `http://localhost:5050`
- **Móvil**: `http://[TU-IP]:5050` (misma red WiFi)

El servidor mostrará automáticamente:
- URL local de acceso
- Código QR para acceso rápido desde móvil
- Estado de los servicios disponibles

---

## 📝 Formatos Soportados

| Tipo | Formatos |
|------|----------|
| **Imágenes** | PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP |
| **Documentos** | PDF, DOCX (salida) |

---

## 🛠️ Funcionalidades Detalladas

### 1. Imágenes a PDF
- Convierte una o múltiples imágenes en un solo archivo PDF
- Mantiene la calidad original de las imágenes
- Ordena las imágenes según la selección

### 2. Unir PDFs (CORREGIDO)
- **Dos métodos de unión** para máxima compatibilidad:
  - Método 1: PdfMerger (estándar)
  - Método 2: PdfWriter (alternativo)
- **Sin duplicación de páginas** - Problema solucionado en v3.2
- Combina documentos de diferentes fuentes
- Preserva el formato original

### 3. PDF a Word (DOCX)
- Extrae texto de archivos PDF
- Mantiene la estructura básica de títulos y párrafos
- Soporta múltiples páginas y documentos

---

## 🔧 Solución de Problemas

### Puerto ocupado
```bash
# Cambia el puerto 5050 en start.py
port = 5050  # Modificar este valor
```

### Error de importación
```bash
# Verifica las dependencias instaladas
pip list | grep -E "Flask|Pillow|PyPDF2|python-docx|qrcode"
```

### PDFs protegidos
> ⚠️ No se pueden procesar PDFs con contraseña

### Móvil no conecta
- Verifica que ambos dispositivos estén en la misma red WiFi
- Comprueba el firewall (puerto 5050)
- Usa la IP correcta mostrada al iniciar

### Error con `--break-system-packages`
> En sistemas que no lo requieran, omite esta bandera

---

## 📋 Requisitos del Sistema

- **Python**: 3.6 o superior
- **Conexión a Internet**: Solo para instalar dependencias
- **Navegador**: Chrome, Firefox, Edge, Safari (versiones actualizadas)
- **Memoria RAM**: 512MB mínimo (recomendado 1GB+)

---

## 📞 Contacto

<div align="center">
  
  **¿Dudas o sugerencias?**
  
  📸 **Instagram**: [@xonidu](https://instagram.com/xonidu)
  
  📘 **Facebook**: [xonidu](https://facebook.com/xonidu)
  
  📧 **Email**: xonidu@gmail.com
  
  👤 **Creador**: Darian Alberto Camacho Salas
  
</div>

