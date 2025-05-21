import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader
import os

def get_desktop_path():
    # Cross-platform: funziona sia su Windows che Linux
    return os.path.join(os.path.expanduser("~"), "Desktop")

def select_file():
    desktop = get_desktop_path()
    filepath = filedialog.askopenfilename(title="Seleziona un file PDF", initialdir=desktop, filetypes=[("PDF Files", "*.pdf")])
    if filepath:
        pdf_path.set(filepath)

def extract_matching_pages():
    path = pdf_path.get()
    keyword = search_string.get().strip()

    if not path or not keyword:
        messagebox.showwarning("Attenzione", "Seleziona un file PDF e inserisci una stringa da cercare.")
        return

    try:
        doc = fitz.open(path)
        matching_pages = []

        for i, page in enumerate(doc):
            text = page.get_text()
            if keyword.lower() in text.lower():
                matching_pages.append(i)

        if not matching_pages:
            messagebox.showinfo("Nessun risultato", "Nessuna pagina contiene la stringa indicata.")
            return

        reader = PdfReader(path)
        writer = PdfWriter()
        for page_num in matching_pages:
            writer.add_page(reader.pages[page_num])

        output_path = os.path.splitext(path)[0] + f"_" + keyword + f"_estratto.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)

        messagebox.showinfo("Successo", f"PDF creato con {len(matching_pages)} pagina/e: {output_path}")
        ## Apri il file PDF estratto sia da windows che da linux
        if os.name == 'posix':  # Linux
            os.system(f'xdg-open "{output_path}"')
        else:  # Windows
            os.startfile(output_path)  # Funziona su Windows
    except Exception as e:
        messagebox.showerror("Errore", str(e))

# GUI
root = tk.Tk()
root.title("PDF Sifter")
root.geometry("900x500")

pdf_path = tk.StringVar()
search_string = tk.StringVar()

tk.Label(root, text="PDF selezionato:").pack(pady=5)
tk.Entry(root, textvariable=pdf_path, width=50).pack(padx=10)
tk.Button(root, text="Sfoglia...", command=select_file).pack(pady=5)

tk.Label(root, text="Stringa da cercare:").pack(pady=5)
tk.Entry(root, textvariable=search_string, width=30).pack()

tk.Button(root, text="Estrai pagine", command=extract_matching_pages).pack(pady=20)

root.mainloop()
