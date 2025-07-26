import os
import tkinter as tk
from tkinter import messagebox
from tkhtmlview import HTMLLabel
from PIL import ImageTk
from controls import zoom_in, zoom_out, go_forward, go_back, on_mousewheel, bind_navigation_controls
from config import load_progress, save_progress
from utils.epub_parser import extract_epub, get_html_paths
from utils.pdf_renderer import render_pdf_page

class EBookReader(tk.Tk):
    def __init__(self, book_path, library_callback=None):
        super().__init__()
        self.title("eBook Reader")
        self.geometry("900x700")
        self.book_path = book_path
        self.book_type = os.path.splitext(book_path)[1].lower()
        self.library_callback = library_callback
        self.zoom_scale = 1.0

        if self.book_type == ".epub":
            self.setup_epub()
        elif self.book_type == ".pdf":
            self.setup_pdf()
        else:
            messagebox.showerror("Error", "Unsupported file type.")
            self.destroy()

        bind_navigation_controls(self)
        back_btn = tk.Button(self, text="Back to Library", command=self.back_to_library)
        back_btn.pack(side="bottom", pady=5)

    def back_to_library(self):
        self.destroy()
        if self.library_callback:
            self.library_callback().mainloop()

    def setup_epub(self):
        opf_path = extract_epub(self.book_path)
        self.html_pages = get_html_paths(opf_path)
        self.current_index = load_progress(self.book_path)

        self.html_view = HTMLLabel(self, html=self.load_html(self.html_pages[self.current_index]), width=100, height=30)
        self.html_view.pack(fill="both", expand=True)

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=5)
        tk.Button(nav, text="Previous", command=self.prev_page).pack(side="left", padx=5)
        tk.Button(nav, text="Next", command=self.next_page).pack(side="left", padx=5)

    def load_html(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def next_page(self):
        if self.current_index < len(self.html_pages) - 1:
            self.current_index += 1
            self.html_view.set_html(self.load_html(self.html_pages[self.current_index]))
            save_progress(self.book_path, self.book_type, self.current_index)

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.html_view.set_html(self.load_html(self.html_pages[self.current_index]))
            save_progress(self.book_path, self.book_type, self.current_index)

    def setup_pdf(self):
        self.pdf_page = load_progress(self.book_path)
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.image_container = self.canvas.create_image(0, 0, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(self, e))
        self.bind("<Configure>", lambda event: self.display_pdf_page())

        nav = tk.Frame(self)
        nav.pack(side="bottom", pady=5)
        tk.Button(nav, text="Previous", command=self.prev_pdf_page).pack(side="left", padx=5)
        tk.Button(nav, text="Next", command=self.next_pdf_page).pack(side="left", padx=5)

        zoom_controls = tk.Frame(self)
        zoom_controls.pack(side="bottom", pady=3)
        tk.Button(zoom_controls, text="🔍 Zoom In", command=lambda: zoom_in(self)).pack(side="left", padx=5)
        tk.Button(zoom_controls, text="🔎 Zoom Out", command=lambda: zoom_out(self)).pack(side="left", padx=5)
        self.zoom_label = tk.Label(zoom_controls, text="Zoom: 100%")
        self.zoom_label.pack(side="left", padx=10)
        self.display_pdf_page()

    def display_pdf_page(self):
        canvas_width = self.canvas.winfo_width() or 900
        scale = (canvas_width / 800) * self.zoom_scale
        image = render_pdf_page(self.book_path, self.pdf_page, scale=scale)
        self.tk_img = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.image_container, image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        if hasattr(self, "zoom_label"):
            self.zoom_label.config(text=f"Zoom: {int(self.zoom_scale * 100)}%")

    def next_pdf_page(self):
        self.pdf_page += 1
        try:
            self.display_pdf_page()
            save_progress(self.book_path, self.book_type, self.pdf_page)
        except:
            self.pdf_page -= 1

    def prev_pdf_page(self):
        if self.pdf_page > 0:
            self.pdf_page -= 1
            self.display_pdf_page()
            save_progress(self.book_path, self.book_type, self.pdf_page)