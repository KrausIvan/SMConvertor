import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SMConvertor")
        
        # Proměnné
        self.input_files = {}
        self.output_folder = tk.StringVar()
        self.quality = tk.IntVar(value=75)
        self.input_formats = set()
        self.selected_formats = {}
        self.supported_output_formats = ['jpeg', 'png', 'bmp', 'tiff', 'gif', 'ico', 'webp']
        self.output_format = tk.StringVar(value='jpeg')
        
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
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Vstupní složka
        input_frame = ttk.LabelFrame(main_frame, text="Vstupní složka", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        ttk.Label(input_frame, text="Vyberte vstupní složku:").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(input_frame, text="Procházet", command=self.browse_input_folder).grid(row=0, column=1, sticky=tk.W)
        
        # Formáty pro převod
        self.formats_frame = ttk.LabelFrame(main_frame, text="Formáty pro převod", padding="10")
        self.formats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Seznam souborů
        files_frame = ttk.LabelFrame(main_frame, text="Vybrané soubory", padding="10")
        files_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        canvas = tk.Canvas(files_frame)
        self.files_frame_inner = ttk.Frame(canvas)
        scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.files_frame_inner, anchor='nw')
        
        self.files_frame_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Výstupní složka
        output_frame = ttk.LabelFrame(main_frame, text="Výstupní nastavení", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        ttk.Label(output_frame, text="Výstupní složka:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_folder, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Procházet", command=self.browse_output_folder).grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(output_frame, text="Kvalita (1-100):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.quality, width=10).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(output_frame, text="Výstupní formát:").grid(row=2, column=0, sticky=tk.W)
        ttk.Combobox(output_frame, textvariable=self.output_format, values=self.supported_output_formats).grid(row=2, column=1, sticky=tk.W)
        
        # Tlačítko pro konverzi
        ttk.Button(output_frame, text="Konvertovat", command=self.convert_images).grid(row=3, column=1, sticky=tk.W)
        
        self.progress = ttk.Progressbar(output_frame, orient='horizontal', mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Logovací pole
        self.log_text = tk.Text(output_frame, height=10, state='disabled')
        self.log_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
    def browse_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_files = {}
            self.input_formats = set()
            self.populate_files_list(folder)
            self.populate_formats()
        
    def populate_files_list(self, folder):
        for widget in self.files_frame_inner.winfo_children():
            widget.destroy()
            
        for root, dirs, files in os.walk(folder):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                self.input_formats.add(ext)
                if ext in self.input_formats:
                    file_path = os.path.join(root, file)
                    var = tk.BooleanVar(value=True)
                    self.input_files[file_path] = var
                    file_frame = ttk.Frame(self.files_frame_inner)
                    file_frame.pack(fill='x', pady=2)
                    
                    chk = ttk.Checkbutton(file_frame, text=file_path, variable=var, command=self.update_format_selections)
                    chk.pack(side='left', fill='x', expand=True)
        
    def populate_formats(self):
        for widget in self.formats_frame.winfo_children():
            widget.destroy()
            
        self.selected_formats = {fmt: tk.BooleanVar(value=True) for fmt in self.input_formats}
        for i, fmt in enumerate(self.input_formats):
            chk = ttk.Checkbutton(self.formats_frame, text=fmt, variable=self.selected_formats[fmt], command=self.update_file_selections)
            chk.grid(row=i//3, column=i%3, sticky=tk.W)
        
    def update_file_selections(self):
        selected_formats = [fmt for fmt, var in self.selected_formats.items() if var.get()]
        for file, var in self.input_files.items():
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in selected_formats:
                var.set(True)
            else:
                var.set(False)
        
    def update_format_selections(self):
        format_counts = {fmt: 0 for fmt in self.input_formats}
        for file, var in self.input_files.items():
            if var.get():
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in format_counts:
                    format_counts[file_ext] += 1
        for fmt, count in format_counts.items():
            self.selected_formats[fmt].set(count > 0)
        
    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
            
    def log_message(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.configure(state='disabled')
        self.log_text.yview(tk.END)

    def convert_images(self):
        output_folder = self.output_folder.get()
        quality = self.quality.get()
        output_format = self.output_format.get().strip('.')
        
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
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.' + output_format)
            
            try:
                with Image.open(input_file) as img:
                    if img.mode in ('RGBA', 'P') and output_format in ['jpeg', 'jpg']:
                        img = img.convert('RGB')
                    img.save(output_file, format=output_format.upper(), quality=quality)
                self.log_message(f'Převedeno: {input_file} -> {output_file}')
            except Exception as e:
                self.log_message(f'Chyba při převodu {input_file}: {e}')
            
            self.progress['value'] = i + 1
            self.root.update_idletasks()
                        
        messagebox.showinfo("Úspěch", "Konverze dokončena!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
