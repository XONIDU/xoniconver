from flask import Flask, request, make_response, render_template_string, flash, redirect, url_for
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
import io
import zipfile
import datetime
import socket

app = Flask(__name__)
app.secret_key = "clave_secreta_para_flask"

# Tamaño máximo razonable por subida (ajusta si quieres).
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_PDF_EXTENSIONS)

# Interfaz simplificada y móvil‑friendly, y título cambiado a XONI‑CONVER.
# He eliminado el campo informativo "Máx archivos (informativo)" según lo solicitado.
HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>XONI-CONVER</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        :root{
            --bg:#f4f4f9;
            --card:#ffffff;
            --accent:#007BFF;
            --muted:#666;
        }
        html,body{height:100%;margin:0;}
        body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; background:var(--bg); color:#222; padding:12px; display:flex; align-items:flex-start; justify-content:center; }
        .box { width:100%; max-width:760px; background:var(--card); padding:18px; border-radius:12px; box-shadow:0 6px 24px rgba(20,20,30,0.06); }
        h1{margin:0 0 12px 0;font-size:1.25rem}
        .row{display:flex;flex-direction:column;gap:8px}
        label{font-weight:600;font-size:0.95rem}
        select,input[type="number"],button{font-size:1rem}
        input[type="file"]{padding:8px}
        button{background:var(--accent);color:#fff;padding:12px;border-radius:8px;border:none;width:100%;font-weight:600}
        .msg { color: #b71c1c; margin: 8px 0; font-size:0.95rem; }
        .hint { font-size:0.9em; color:var(--muted); margin:8px 0 16px 0; }
        .small { font-size:0.85em; color:var(--muted); margin-top:12px; }
        .flex{display:flex;gap:8px}
        @media(min-width:600px){
            .flex-row{display:flex;gap:12px}
            .flex-row > *{flex:1}
            .row{gap:12px}
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>XONI-CONVER</h1>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="msg">
              {% for m in messages %}
                <div>{{ m }}</div>
              {% endfor %}
            </div>
          {% endif %}
        {% endwith %}

        <p class="hint">Conversor ligero: imágenes → PDF, unir PDFs y extraer texto PDF → Word. Diseñado para ser apto en móviles (interfaz responsive).</p>

        <form method="POST" enctype="multipart/form-data">
            <div class="row">
                <label for="conversion">Elige conversión:</label>
                <select name="conversion" id="conversion" required>
                    <option value="images_to_pdf">Imágenes (PNG/JPEG) → PDF</option>
                    <option value="merge_pdfs">Unir varios PDFs → PDF único</option>
                    <option value="pdf_to_docx">PDF → Word (.docx) (extracción de texto)</option>
                </select>

                <label for="files">Sube tus archivos (múltiples permitidos):</label>
                <!-- accept ayuda a móviles a filtrar tipos -->
                <input type="file" name="files" id="files" multiple required accept=".pdf,image/png,image/jpeg">

                <button type="submit">Convertir</button>

                <div class="small">Nota: No guardamos archivos permanentemente en el servidor; todo se procesa en memoria y se borra al terminar.</div>
            </div>
        </form>
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
        # Asegurarse de posicionar al inicio
        try:
            f.stream.seek(0)
        except Exception:
            pass
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

def pdf_to_docx(files):
    docs = []
    for f in files:
        if f.filename == "" or not is_pdf_filename(f.filename):
            continue
        try:
            f.stream.seek(0)
        except Exception:
            pass
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
                for line in text.splitlines():
                    doc.add_paragraph(line)
            doc.add_page_break()
        name = f.filename.rsplit(".", 1)[0] + ".docx"
        out = io.BytesIO()
        doc.save(out)
        out.seek(0)
        docs.append((name, out.read()))
    if not docs:
        raise ValueError("No hay PDFs válidos para convertir a Word.")
    if len(docs) == 1:
        name, data = docs[0]
        return ("single", (name, data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
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
        files = request.files.getlist("files")
        if not files or files == [None]:
            flash("No se subió ningún archivo.")
            return redirect(url_for("index"))

        if all((f.filename == "" or not allowed_filename(f.filename)) for f in files):
            flash("Ninguno de los archivos tiene una extensión permitida.")
            return redirect(url_for("index"))

        try:
            if conversion == "images_to_pdf":
                imgs = [f for f in files if is_image_filename(f.filename)]
                result_type, payload = images_to_pdf(imgs)

            elif conversion == "merge_pdfs":
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdfs_merge(pdfs)

            elif conversion == "pdf_to_docx":
                pdfs = [f for f in files if is_pdf_filename(f.filename)]
                result_type, payload = pdf_to_docx(pdfs)

            else:
                flash("Conversión no soportada.")
                return redirect(url_for("index"))

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
            flash("Error durante la conversión: " + str(e))
            return redirect(url_for("index"))

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5050
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"
    print(f"* XONI-CONVER running on http://{local_ip}:{port} and on all interfaces {host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)
