import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SMConvertor")
        
        # Proměnné
        self.input_files = {}
        self.output_folder = tk.StringVar()
        self.quality = tk.IntVar(value=75)
        self.input_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.ico', '.webp']
        self.selected_formats = {fmt: tk.BooleanVar(value=True) for fmt in self.input_formats}
        self.output_format = tk.StringVar(value='.webp')
        
        # Nastavení stylu
        self.set_style()
        
        # GUI Layout
        self.create_widgets()
        
    def set_style(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')  # Use a modern theme
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', foreground='#333')
        style.configure('TEntry', fieldbackground='white', background='white', foreground='#333')
        style.configure('TButton', background='#ec6608', foreground='white')
        style.map('TButton', background=[('active', '#ec6608'), ('disabled', '#f0f0f0')], foreground=[('disabled', '#a3a3a3')])
        style.configure('TCheckbutton', background='white', foreground='#333')
        style.configure('TCombobox', fieldbackground='white', background='white', foreground='#333')
        style.configure('Horizontal.TProgressbar', troughcolor='white', background='#ec6608')
        
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Vstupní složka:").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(frame, text="Procházet", command=self.browse_input_folder).grid(row=0, column=2, sticky=tk.W)
        
        self.files_frame = ttk.Frame(frame)
        self.files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Label(frame, text="Výstupní složka:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.output_folder, width=40).grid(row=2, column=1, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Procházet", command=self.browse_output_folder).grid(row=2, column=2, sticky=tk.W)
        
        ttk.Label(frame, text="Kvalita (1-100):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.quality, width=10).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="Formáty pro převod:").grid(row=4, column=0, sticky=tk.W)
        formats_frame = ttk.Frame(frame)
        formats_frame.grid(row=4, column=1, sticky=tk.W)
        for i, fmt in enumerate(self.input_formats):
            ttk.Checkbutton(formats_frame, text=fmt, variable=self.selected_formats[fmt]).grid(row=i//3, column=i%3, sticky=tk.W)
        
        ttk.Label(frame, text="Výstupní formát:").grid(row=5, column=0, sticky=tk.W)
        ttk.Combobox(frame, textvariable=self.output_format, values=self.input_formats).grid(row=5, column=1, sticky=tk.W)
        
        ttk.Button(frame, text="Konvertovat", command=self.convert_images).grid(row=6, column=1, sticky=tk.W)
        
        self.progress = ttk.Progressbar(frame, orient='horizontal', mode='determinate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
    def browse_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_files = {}
            self.populate_files_list(folder)
        
    def populate_files_list(self, folder):
        for widget in self.files_frame.winfo_children():
            widget.destroy()
            
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(tuple(self.input_formats)):
                    file_path = os.path.join(root, file)
                    var = tk.BooleanVar(value=True)
                    self.input_files[file_path] = var
                    chk = ttk.Checkbutton(self.files_frame, text=file_path, variable=var)
                    chk.pack(anchor='w')
        
    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
            
    def convert_images(self):
        output_folder = self.output_folder.get()
        quality = self.quality.get()
        output_format = self.output_format.get()
        selected_formats = [fmt for fmt, var in self.selected_formats.items() if var.get()]
        
        if not self.input_files or not output_folder:
            messagebox.showerror("Chyba", "Vyberte prosím vstupní složku a výstupní složku.")
            return
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        files_to_convert = [file for file, var in self.input_files.items() if var.get()]
        
        self.progress['maximum'] = len(files_to_convert)
        
        for i, input_file in enumerate(files_to_convert):
            relative_path = os.path.relpath(os.path.dirname(input_file), os.path.dirname(list(self.input_files.keys())[0]))
            output_dir = os.path.join(output_folder, relative_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + output_format)
            
            try:
                with Image.open(input_file) as img:
                    img.save(output_file, quality=quality)
                print(f'Převedeno: {input_file} -> {output_file}')
            except Exception as e:
                print(f'Chyba při převodu {input_file}: {e}')
            
            self.progress['value'] = i + 1
            self.root.update_idletasks()
                        
        messagebox.showinfo("Úspěch", "Konverze dokončena!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
