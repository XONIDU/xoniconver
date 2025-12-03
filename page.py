from flask import Flask, request, make_response, render_template_string, flash, redirect, url_for
from PIL import Image
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
import io
import zipfile
import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_para_flask"

# Tamaño máximo razonable por subida (ajusta si quieres). Si prefieres "sin límite" quita esta línea,
# pero cuidad con memoria/DoS.
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_PDF_EXTENSIONS)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>XONIDU conversión</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; background:#f4f4f9; color:#333; padding:2em; }
        .box { max-width:900px; margin:0 auto; background:white; padding:20px; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.08); }
        input[type="file"]{ margin:10px 0; width:100%; }
        select, button{ margin:8px 0; padding:10px; border-radius:6px; }
        button{ background:#007BFF; color:white; border:none; cursor:pointer; }
        .msg { color: red; margin: 0.5em 0; }
        .hint { font-size:0.9em; color:#666; }
        .small { font-size:0.85em; color:#666; }
    </style>
</head>
<body>
    <div class="box">
        <h1>XONIDU Convertidor: imágenes ↔ PDF, PDF → Word, PDF → PNG/JPEG y más</h1>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="msg">
              {% for m in messages %}
                <div>{{ m }}</div>
              {% endfor %}
            </div>
          {% endif %}
        {% endwith %}

        <p class="hint">Selecciona uno o varios archivos. No guardamos los archivos permanentemente en el servidor; todo se procesa en memoria y se borra al terminar.</p>

        <form method="POST" enctype="multipart/form-data">
            <label for="conversion">Elige conversión:</label><br>
            <select name="conversion" id="conversion" required>
                <option value="images_to_pdf">Imágenes (PNG/JPEG) → PDF</option>
                <option value="pdf_to_png">PDF → Imágenes PNG</option>
                <option value="pdf_to_jpeg">PDF → Imágenes JPEG</option>
                <option value="pdf_to_docx">PDF → Word (.docx) (extracción de texto)</option>
                <option value="merge_pdfs">Unir varios PDFs → PDF único</option>
                <option value="pdf_to_single_images">PDF(s) → ZIP con imágenes (cada página como imagen)</option>
            </select><br>

            <label for="files">Sube tus archivos (múltiples permitidos):</label><br>
            <input type="file" name="files" id="files" multiple required><br>

            <label for="dpi">DPI para conversiones a imagen (solo PDF→imagen):</label><br>
            <input type="number" name="dpi" id="dpi" min="72" max="600" value="200"><br>

            <button type="submit">Convertir</button>
        </form>

        <p class="small">Nota: PDF → Word intenta extraer el texto (sin preservar diseño complejo). Para PDF→imagen se usa pdf2image (requiere poppler instalado en el servidor).</p>
    </div>
</body>
</html>
"""

def allowed_filename(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def is_image_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def is_pdf_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_PDF_EXTENSIONS

def images_to_pdf(files):
    # files: list of FileStorage image streams
    pil_images = []
    for f in files:
        if f.filename == "" or not is_image_filename(f.filename):
            continue
        img = Image.open(f.stream).convert("RGB")
        pil_images.append(img)

    if not pil_images:
        raise ValueError("No hay imágenes válidas para convertir a PDF.")

    output = io.BytesIO()
    first, rest = pil_images[0], pil_images[1:]
    first.save(output, format="PDF", save_all=True, append_images=rest)
    output.seek(0)
    return ("single", ("converted.pdf", output.read(), "application/pdf"))

def pdfs_merge(files):
    writer = PdfWriter()
    count = 0
    for f in files:
        if f.filename == "" or not is_pdf_filename(f.filename):
            continue
        reader = PdfReader(f.stream)
        for page in reader.pages:
            writer.add_page(page)
        count += 1
    if count == 0:
        raise ValueError("No hay PDFs válidos para unir.")
    out = io.BytesIO()
    writer.write(out)
    out.seek(0)
    return ("single", ("merged.pdf", out.read(), "application/pdf"))

def pdfs_to_images_zip(files, image_format="PNG", dpi=200):
    # produce a zip containing images named <originalname>_page_001.png etc.
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        any_added = False
        for f in files:
            if f.filename == "" or not is_pdf_filename(f.filename):
                continue
            pdf_bytes = f.read()
            # convert_from_bytes returns list of PIL images
            pages = convert_from_bytes(pdf_bytes, dpi=dpi)
            base = f.filename.rsplit(".", 1)[0]
            for i, img in enumerate(pages, start=1):
                img_bytes = io.BytesIO()
                fmt = "PNG" if image_format.upper() == "PNG" else "JPEG"
                # For JPEG, set quality
                if fmt == "JPEG":
                    img.save(img_bytes, format=fmt, quality=90)
                else:
                    img.save(img_bytes, format=fmt)
                img_bytes.seek(0)
                name = f"{base}_page_{i:03d}.{fmt.lower()}"
                zf.writestr(name, img_bytes.read())
                any_added = True
        if not any_added:
            raise ValueError("No hay PDFs válidos para convertir a imágenes.")
    zip_buffer.seek(0)
    return ("zip", ("pdf_images_%s.zip" % datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"), zip_buffer.read(), "application/zip"))

def pdf_to_docx(files):
    # For each pdf uploaded, extract text and produce a .docx.
    # If multiple PDFs → return a zip with each docx.
    docs = []
    for f in files:
        if f.filename == "" or not is_pdf_filename(f.filename):
            continue
        reader = PdfReader(f.stream)
        doc = Document()
        any_text = False
        for page in reader.pages:
            text = ""
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            if text.strip():
                any_text = True
                # preserve paragraphs by splitting lines
                for line in text.splitlines():
                    doc.add_paragraph(line)
            # add page break between pages
            doc.add_page_break()
        name = f.filename.rsplit(".", 1)[0] + ".docx"
        # save to bytes
        out = io.BytesIO()
        doc.save(out)
        out.seek(0)
        docs.append((name, out.read()))
    if not docs:
        raise ValueError("No hay PDFs válidos para convertir a Word.")
    if len(docs) == 1:
        name, data = docs[0]
        return ("single", (name, data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    # multiple -> zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in docs:
            zf.writestr(name, data)
    zip_buffer.seek(0)
    return ("zip", ("pdf_to_docx_%s.zip" % datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"), zip_buffer.read(), "application/zip"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conversion = request.form.get("conversion")
        try:
            dpi = int(request.form.get("dpi", 200))
        except Exception:
            dpi = 200

        files = request.files.getlist("files")
        if not files or files == [None]:
            flash("No se subió ningún archivo.")
            return redirect(url_for("index"))

        # Validate at least one filename valid
        if all((f.filename == "" or not allowed_filename(f.filename)) for f in files):
            flash("Ninguno de los archivos tiene una extensión permitida.")
            return redirect(url_for("index"))

        try:
            if conversion == "images_to_pdf":
                # Filter images only
                imgs = [f for f in files if is_image_filename(f.filename)]
                result_type, payload = images_to_pdf(imgs)

            elif conversion == "merge_pdfs":
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdfs_merge(pdfs)

            elif conversion == "pdf_to_png":
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdfs_to_images_zip(pdfs, image_format="PNG", dpi=dpi)

            elif conversion == "pdf_to_jpeg":
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdfs_to_images_zip(pdfs, image_format="JPEG", dpi=dpi)

            elif conversion == "pdf_to_docx":
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdf_to_docx(pdfs)

            elif conversion == "pdf_to_single_images":
                # similar to pdf_to_png but name is explicit
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdfs_to_images_zip(pdfs, image_format="PNG", dpi=dpi)

            else:
                flash("Conversión no soportada.")
                return redirect(url_for("index"))

            # payload handling
            if result_type == "single":
                filename, data, mime = payload
                response = make_response(data)
                response.headers.set("Content-Type", mime)
                response.headers.set("Content-Disposition", "attachment", filename=filename)
                return response
            elif result_type == "zip":
                filename, data, mime = payload
                response = make_response(data)
                response.headers.set("Content-Type", mime)
                response.headers.set("Content-Disposition", "attachment", filename=filename)
                return response
            else:
                flash("Resultado desconocido.")
                return redirect(url_for("index"))

        except Exception as e:
            # No mostrar detalles internos al usuario
            flash("Error durante la conversión: " + str(e))
            return redirect(url_for("index"))

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
