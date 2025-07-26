# utils/pdf_renderer.py

import fitz  # PyMuPDF
from PIL import Image

def render_pdf_page(pdf_path, page_num, scale=1.0):
    doc = fitz.open(pdf_path)
    if page_num >= len(doc):  # Prevent out-of-range crash
        page_num = len(doc) - 1

    page = doc.load_page(page_num)
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat)

    # Convert to a proper PIL.Image object (RGB)
    mode = "RGB" if pix.alpha == 0 else "RGBA"
    image = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

    return image
