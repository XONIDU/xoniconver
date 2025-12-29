# XONI-CONVER v3.2

Servicio web para convertir archivos:
- Imágenes → PDF
- Unir múltiples PDFs → PDF único (corregido sin duplicación)
- Extraer texto de PDF → Word (.docx)

Interfaz responsive para PC y móvil. Escucha en `0.0.0.0:5050`

---

## 📦 Instalación Rápida

### Arch Linux
```bash
sudo pacman -Syu python-pip libjpeg-turbo zlib tk
pip install Flask Pillow PyPDF2 python-docx --break-system-packages
```

### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk libjpeg-dev zlib1g-dev
pip3 install Flask Pillow PyPDF2 python-docx --break-system-packages
```

### Windows
```bash
pip install Flask Pillow PyPDF2 python-docx
```

---

## 🚀 Ejecución

```bash
python page.py
```

Accede desde:
- PC: `http://localhost:5050`
- Móvil: `http://TU-IP:5050` (misma red WiFi)

---

## ✨ Características

- ✅ PDF Merge corregido (sin duplicación)
- 🖼️ Convierte imágenes a PDF
- 📄 Extrae texto de PDF a Word
- 📱 Interfaz responsive para PC/móvil
- 🔒 Procesamiento seguro en memoria
- ⚡ Sin límites de tamaño

---

## 📝 Formatos Soportados

**Imágenes:** PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP  
**Documentos:** PDF, DOCX

---

## 🛠️ Solución de Problemas

- **Puerto ocupado:** Cambia el puerto 5050 en `page.py`
- **Error de importación:** Verifica las dependencias instaladas
- **PDFs protegidos:** No se pueden procesar PDFs con contraseña
- **Móvil no conecta:** Verifica firewall y IP correcta

---

**XONI-CONVER v3.2** • by XONIDU • Procesamiento seguro