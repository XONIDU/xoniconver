from flask import Flask, request, make_response, render_template, flash, redirect, url_for
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from docx import Document
import io
import zipfile
import datetime
import socket
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename
import qrcode
from io import StringIO

app = Flask(__name__)
app.secret_key = "clave_secreta_xoni_conver_pc"

# Desactivar límite de tamaño
app.config['MAX_CONTENT_LENGTH'] = None

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_PDF_EXTENSIONS)

def generar_qr_terminal(texto):
    """
    Genera un código QR en ASCII para mostrar en terminal
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=2,
        border=1
    )
    qr.add_data(texto)
    qr.make(fit=True)
    
    # Crear imagen QR en ASCII para terminal
    qr_ascii = StringIO()
    qr.print_ascii(out=qr_ascii, invert=True)
    return qr_ascii.getvalue()

def allowed_filename(filename: str) -> bool:
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def is_image_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def is_pdf_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_PDF_EXTENSIONS

def images_to_pdf(files):
    """Convert images to PDF"""
    pil_images = []
    temp_dirs = []
    
    try:
        for f in files:
            if not is_image_filename(f.filename):
                continue
            
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, secure_filename(f.filename))
            f.save(temp_path)
            temp_dirs.append(temp_dir)
            
            try:
                img = Image.open(temp_path).convert("RGB")
                pil_images.append(img)
            except Exception as e:
                print(f"Error procesando imagen {f.filename}: {e}")
                continue
        
        if not pil_images:
            raise ValueError("No hay imágenes válidas para convertir.")
        
        output = io.BytesIO()
        if len(pil_images) == 1:
            pil_images[0].save(output, format="PDF")
        else:
            first, rest = pil_images[0], pil_images[1:]
            first.save(output, format="PDF", save_all=True, append_images=rest)
        
        output.seek(0)
        return ("single", ("imagenes_a_pdf.pdf", output.read(), "application/pdf"))
        
    finally:
        for temp_dir in temp_dirs:
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

def pdfs_merge_v1(files):
    """Merge PDFs usando PdfMerger - Método 1"""
    merger = PdfMerger()
    temp_dirs = []
    
    try:
        for idx, f in enumerate(files):
            if not is_pdf_filename(f.filename):
                continue
            
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, secure_filename(f.filename))
            f.save(temp_path)
            temp_dirs.append(temp_dir)
            
            try:
                # Usar PdfMerger que es más robusto para unir
                merger.append(temp_path)
                print(f"✅ PDF {idx+1} agregado: {f.filename}")
            except Exception as e:
                print(f"❌ Error con PdfMerger para {f.filename}: {e}")
                raise
        
        if len(merger.pages) == 0:
            raise ValueError("No se pudieron procesar archivos PDF válidos.")
        
        print(f"📊 Total de páginas: {len(merger.pages)}")
        
        output = io.BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)
        
        return ("single", ("pdfs_combinados.pdf", output.read(), "application/pdf"))
        
    finally:
        for temp_dir in temp_dirs:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass

def pdfs_merge_v2(files):
    """Merge PDFs usando PdfWriter - Método 2 (alternativo)"""
    writer = PdfWriter()
    processed_pages = 0
    
    try:
        for idx, f in enumerate(files):
            if not is_pdf_filename(f.filename):
                continue
            
            # Guardar en memoria directamente
            f.seek(0)
            pdf_bytes = f.read()
            pdf_stream = io.BytesIO(pdf_bytes)
            
            try:
                reader = PdfReader(pdf_stream)
                
                # Verificar páginas
                if len(reader.pages) == 0:
                    print(f"⚠️ PDF vacío: {f.filename}")
                    continue
                
                # Agregar TODAS las páginas
                for page in reader.pages:
                    writer.add_page(page)
                    processed_pages += 1
                
                print(f"✅ PDF {idx+1}: {f.filename} ({len(reader.pages)} páginas)")
                
            except Exception as e:
                print(f"❌ Error leyendo PDF {f.filename}: {e}")
                continue
        
        if processed_pages == 0:
            raise ValueError("No se pudieron procesar archivos PDF válidos.")
        
        print(f"📊 Total final de páginas: {processed_pages}")
        
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        return ("single", ("pdfs_unidos.pdf", output.read(), "application/pdf"))
        
    finally:
        try:
            writer.close()
        except:
            pass

def pdf_to_docx(files):
    """Convert PDF(s) to single DOCX file"""
    doc = Document()
    temp_dirs = []
    
    try:
        doc.add_heading('Documento Convertido de PDF', 0)
        text_extracted = False
        
        for idx, f in enumerate(files):
            if not is_pdf_filename(f.filename):
                continue
            
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, secure_filename(f.filename))
            f.save(temp_path)
            temp_dirs.append(temp_dir)
            
            try:
                reader = PdfReader(temp_path)
                
                if len(files) > 1:
                    doc.add_heading(f"PDF: {f.filename}", level=2)
                
                for page_num, page in enumerate(reader.pages, 1):
                    try:
                        text = page.extract_text()
                        if text and text.strip():
                            text_extracted = True
                            
                            if len(reader.pages) > 1:
                                doc.add_heading(f"Página {page_num}", level=3)
                            
                            doc.add_paragraph(text)
                            
                            if page_num < len(reader.pages):
                                doc.add_page_break()
                    except:
                        continue
                
                if idx < len(files) - 1:
                    doc.add_heading("─" * 50, level=2)
                    
            except Exception as e:
                doc.add_paragraph(f"Error procesando {f.filename}: {str(e)}")
                continue
        
        if not text_extracted:
            doc.add_paragraph("No se pudo extraer texto de los PDFs.")
        
        doc_buffer = io.BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        
        if len(files) == 1:
            base_name = files[0].filename.rsplit(".", 1)[0]
            filename = f"{base_name}_convertido.docx"
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pdfs_combinados_{timestamp}.docx"
        
        return ("single", (filename, doc_buffer.read(), 
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
        
    finally:
        for temp_dir in temp_dirs:
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conversion = request.form.get("conversion")
        uploaded_files = request.files.getlist("files")
        
        # Filtrar archivos válidos
        valid_files = []
        for f in uploaded_files:
            if f and f.filename and allowed_filename(f.filename):
                valid_files.append(f)
        
        if not valid_files:
            flash("No se subió ningún archivo válido.", "error")
            return redirect(url_for("index"))
        
        try:
            if conversion == "images_to_pdf":
                imgs = [f for f in valid_files if is_image_filename(f.filename)]
                if not imgs:
                    flash("No se encontraron imágenes válidas.", "error")
                    return redirect(url_for("index"))
                result_type, payload = images_to_pdf(imgs)

            elif conversion == "merge_pdfs":
                pdfs = [f for f in valid_files if is_pdf_filename(f.filename)]
                if len(pdfs) < 2:
                    flash("Se requieren al menos 2 archivos PDF para unir.", "error")
                    return redirect(url_for("index"))
                
                # Intentar primero con PdfMerger, luego con PdfWriter
                try:
                    print("🔄 Intentando unir PDFs con PdfMerger (método 1)...")
                    result_type, payload = pdfs_merge_v1(pdfs)
                except Exception as e1:
                    print(f"❌ PdfMerger falló: {e1}")
                    print("🔄 Intentando con PdfWriter (método 2)...")
                    try:
                        result_type, payload = pdfs_merge_v2(pdfs)
                    except Exception as e2:
                        flash(f"Error al unir PDFs: {e2}", "error")
                        return redirect(url_for("index"))

            elif conversion == "pdf_to_docx":
                pdfs = [f for f in valid_files if is_pdf_filename(f.filename)]
                if not pdfs:
                    flash("No se encontraron archivos PDF.", "error")
                    return redirect(url_for("index"))
                result_type, payload = pdf_to_docx(pdfs)

            else:
                flash("Tipo de conversión no válido.", "error")
                return redirect(url_for("index"))

            # Devolver archivo
            if result_type == "single":
                filename, data, mime = payload
                response = make_response(data)
                response.headers.set("Content-Type", mime)
                response.headers.set("Content-Disposition", "attachment", filename=filename)
                return response
                
            else:
                flash("Error en la conversión.", "error")
                return redirect(url_for("index"))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("index"))

    return render_template('index.html')

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5050
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"
    
    # Limpiar pantalla
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("=" * 60)
    print("XONI-CONVER v3.2 - Conversor Universal (CORREGIDO)")
    print("=" * 60)
    print(f"🌐 URL Local:      http://{local_ip}:{port}")
    print(f"📱 Móvil:          Usa la misma IP en tu red WiFi")
    print("=" * 60)
    
    # Generar QR con la URL
    url_completa = f"http://{local_ip}:{port}"
    print("\n📱 ESCANEA ESTE CÓDIGO QR PARA ACCEDER DESDE TU MÓVIL:\n")
    print(generar_qr_terminal(url_completa))
    print("\n" + "=" * 60)
    
    print("✨ Características:")
    print("   • 2 métodos para unir PDFs (sin duplicación)")
    print("   • Interfaz responsive para PC y móvil")
    print("   • Sin límites de tamaño")
    print("   • Procesamiento seguro en memoria")
    print("=" * 60)
    
    app.run(
        host=host, 
        port=port, 
        debug=False,
        threaded=True
    )
