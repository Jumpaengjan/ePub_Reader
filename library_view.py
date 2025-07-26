import os
import tkinter as tk
from tkinter import filedialog, messagebox
from config import load_last_folder, save_last_folder
from reader_view import EBookReader

class LibraryView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Library Folder")
        self.geometry("600x400")
        self.books = []

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10, padx=10, fill="x")

        self.folder_path = tk.StringVar()
        path_entry = tk.Entry(input_frame, textvariable=self.folder_path, width=50)
        path_entry.pack(side="left", expand=True, fill="x")

        browse_btn = tk.Button(input_frame, text="Browse", command=self.select_folder)
        browse_btn.pack(side="left", padx=5)

        refresh_btn = tk.Button(input_frame, text="Scan", command=self.scan_books)
        refresh_btn.pack(side="left")

        self.book_listbox = tk.Listbox(self, font=("Arial", 12))
        self.book_listbox.pack(padx=10, pady=10, expand=True, fill="both")
        self.book_listbox.bind("<Double-Button-1>", self.open_selected_book)

        last_folder = load_last_folder()
        if last_folder:
            self.folder_path.set(last_folder)
            self.scan_books()

    def select_folder(self):
        path = filedialog.askdirectory(title="Choose Library Folder")
        if path:
            self.folder_path.set(path)
            save_last_folder(path)
            self.scan_books()

    def scan_books(self):
        folder = self.folder_path.get()
        if not os.path.isdir(folder):
            messagebox.showerror("Invalid Path", "That path does not exist.")
            return

        self.books.clear()
        self.book_listbox.delete(0, tk.END)

        for filename in os.listdir(folder):
            if filename.endswith(".epub") or filename.endswith(".pdf"):
                full_path = os.path.join(folder, filename)
                self.books.append(full_path)
                self.book_listbox.insert(tk.END, filename)

    def open_selected_book(self, event):
        selected = self.book_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        book_path = self.books[index]
        self.destroy()
        reader = EBookReader(book_path, library_callback=self.__class__)
        reader.mainloop()