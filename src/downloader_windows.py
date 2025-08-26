"""
Iker2YT - Descargador de YouTube
Un descargador simple con interfaz gráfica para usuarios no técnicos.
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import yt_dlp
import threading
import os
import sys
from pathlib import Path


class YouTubeDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.download_path = str(Path.home() / "Downloads")
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.root.title("IkerDown - Descargador YT del fan #1 de Pedro Sánchez")
        self.root.geometry("500x300")
        self.root.minsize(450, 250)
        self.root.resizable(True, True)
        self.root.configure(bg='white')
        
        # Configurar el icono si existe
        icon_path = self.get_icon_path()
        if icon_path and os.path.exists(icon_path):
            try:
                if sys.platform == "win32":
                    self.root.iconbitmap(icon_path)
                elif sys.platform == "darwin":
                    png_path = icon_path.replace('.ico', '_preview.png')
                    if os.path.exists(png_path):
                        icon_image = tk.PhotoImage(file=png_path)
                        self.root.iconphoto(True, icon_image)
                    else:
                        self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"No se pudo cargar el icono: {e}")
        
        self.center_window()
        
    def create_widgets(self):
        """Crea interfaz compacta y minimalista"""
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Logo (intentar cargar, si no existe usar texto)
        try:
            logo_path = self.get_logo_path()
            if logo_path and os.path.exists(logo_path):
                logo_image = tk.PhotoImage(file=logo_path)
                logo_image = logo_image.subsample(2, 2)
                logo_label = tk.Label(main_frame, image=logo_image, bg='white')
                logo_label.image = logo_image
                logo_label.pack(pady=(0, 5))
            else:
                raise FileNotFoundError("Logo no encontrado")
        except:
            # Fallback a texto si no hay logo
            logo_label = tk.Label(
                main_frame, 
                text="IkerDown", 
                font=('Arial', 18, 'bold'),
                fg="#DC143C",
                bg='white'
            )
            logo_label.pack(pady=(0, 5))

        # Mensaje de bienvenida
        welcome_label = tk.Label(
            main_frame, 
            text="¡Importante! - Usando este servicio financias la campaña de Sanchez para las generales de 2027", 
            font=('Arial', 10), 
            fg='orange',
            bg='white',
            wraplength=450
        )
        welcome_label.pack(pady=(0, 10))

        # Primera línea: URL + Botón Descargar
        first_line = tk.Frame(main_frame, bg='white')
        first_line.pack(fill=tk.X, pady=(0, 10))
        
        # Campo URL
        self.url_entry = tk.Entry(
            first_line, 
            font=('Arial', 12),
            relief=tk.SOLID,
            bd=1,
            bg='white',
            fg='#999999'
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        # Configurar placeholder
        self.placeholder_text = "Pega aquí la URL de YouTube..."
        self.url_entry.insert(0, self.placeholder_text)
        self.url_entry.bind('<FocusIn>', self.on_url_focus_in)
        self.url_entry.bind('<FocusOut>', self.on_url_focus_out)

        # Botón descargar
        self.download_button = tk.Button(
            first_line,
            text="SUUU",
            command=self.start_download,
            font=('Arial', 12, 'bold'),
            bg="#DC143C",
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            width=8
        )
        self.download_button.pack(side=tk.RIGHT, padx=(10, 0), ipady=8)
        
        # Segunda línea: Calidad + Directorio
        second_line = tk.Frame(main_frame, bg='white')
        second_line.pack(fill=tk.X, pady=(0, 10))
        
        # Calidad
        quality_frame = tk.Frame(second_line, bg='white')
        quality_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(quality_frame, text="Calidad:", font=('Arial', 10), bg='white').pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar(value="Máxima (1080p)")
        self.quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["Máxima (1080p)", "720p", "480p", "Solo audio (MP3)"],
            state="readonly",
            width=15,
            font=('Arial', 9)
        )
        self.quality_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Directorio
        dir_frame = tk.Frame(second_line, bg='white')
        dir_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        tk.Label(dir_frame, text="Guardar en:", font=('Arial', 10), bg='white').pack(side=tk.LEFT)
        
        self.dir_button = tk.Button(
            dir_frame,
            text=self.get_short_path(self.download_path, 15),
            command=self.change_destination,
            font=('Arial', 9),
            bg='white',
            fg='#666666',
            relief=tk.SOLID,
            bd=1,
            cursor="hand2"
        )
        self.dir_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Área de progreso
        progress_frame = tk.Frame(main_frame, bg='white')
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Estado
        self.status_label = tk.Label(
            progress_frame,
            text="Listo para descargar",
            font=('Arial', 9),
            fg="#666666",
            bg='white'
        )
        self.status_label.pack()
    
    def get_short_path(self, path, max_length=25):
        """Acorta la ruta para mostrar"""
        if len(path) > max_length:
            return "..." + path[-(max_length-3):]
        return path
        
    def get_icon_path(self):
        """Obtiene la ruta del icono"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, 'assets', 'icon.ico')
    
    def get_logo_path(self):
        """Obtiene la ruta del logo"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Intentar diferentes nombres de logo
        possible_logos = ['logo.png', 'logo_new.png', 'icon.png']
        for logo_name in possible_logos:
            logo_path = os.path.join(base_path, 'assets', logo_name)
            if os.path.exists(logo_path):
                return logo_path
        return None
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def on_url_focus_in(self, event):
        """Maneja cuando el usuario hace clic en el campo URL"""
        if self.url_entry.get() == self.placeholder_text:
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg='black')
    
    def on_url_focus_out(self, event):
        """Maneja cuando el usuario sale del campo URL"""
        if not self.url_entry.get().strip():
            self.url_entry.insert(0, self.placeholder_text)
            self.url_entry.config(fg='#999999')

    def change_destination(self):
        """Cambia el directorio de destino"""
        new_path = filedialog.askdirectory(
            title="Selecciona dónde guardar los videos",
            initialdir=self.download_path
        )
        if new_path:
            self.download_path = new_path
            self.dir_button.config(text=self.get_short_path(new_path, 15))
        
    def start_download(self):
        """Inicia la descarga en un hilo separado"""
        url = self.url_entry.get().strip()
        
        if not url or url == self.placeholder_text:
            messagebox.showerror("Error", "Por favor, pega la URL del video de YouTube.")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Error", "La URL no parece ser de YouTube. Por favor, verifica la URL.")
            return
        
        self.set_downloading_state(True)
        download_thread = threading.Thread(target=self.download_video, args=(url,), daemon=True)
        download_thread.start()
        
    def is_valid_youtube_url(self, url):
        """Valida si la URL es de YouTube"""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        return any(domain in url.lower() for domain in youtube_domains)
        
    def set_downloading_state(self, downloading):
        """Cambia el estado de la interfaz durante descarga"""
        if downloading:
            self.download_button.config(state=tk.DISABLED, text="...")
            self.progress_var.set(0)
            self.status_label.config(text="Iniciando descarga...", fg="#FF6600")
        else:
            self.download_button.config(state=tk.NORMAL, text="SUUU")
            self.progress_var.set(0)
            self.status_label.config(text="Listo para descargar", fg="#666666")
            
    def download_video(self, url):
        """Descarga el video con yt-dlp"""
        try:
            selected_quality = self.quality_var.get()
            
            quality_map = {
                "Máxima (1080p)": (
                    "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/"
                    "bestvideo[height<=1080]+bestaudio/"
                    "best[height<=1080][ext=mp4]/"
                    "best[height<=1080]/"
                    "best"
                ),
                "720p": (
                    "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/"
                    "bestvideo[height<=720]+bestaudio/"
                    "best[height<=720][ext=mp4]/"
                    "best[height<=720]"
                ),
                "480p": (
                    "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/"
                    "bestvideo[height<=480]+bestaudio/"
                    "best[height<=480][ext=mp4]/"
                    "best[height<=480]"
                ),
                "Solo audio (MP3)": "bestaudio[ext=m4a]/bestaudio/best"
            }
            
            format_selector = quality_map.get(selected_quality, quality_map["Máxima (1080p)"])
            
            if selected_quality == "Solo audio (MP3)":
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                postprocessors = []
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(self.download_path, "%(title)s.%(ext)s"),
                'progress_hooks': [self.progress_hook],
                'postprocessors': postprocessors,
                'extract_flat': False,
                'merge_output_format': 'mp4',
                'prefer_ffmpeg': True,
                'verbose': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status("Obteniendo información del video...")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Video')
                
                self.update_status(f"Descargando: {video_title}")
                ydl.download([url])
                
            self.root.after(0, self.download_success, video_title)
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, self.download_error, error_msg)
            
    def progress_hook(self, d):
        """Hook para actualizar progreso"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.root.after(0, self.update_progress, percent)
            
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            self.root.after(0, self.update_status, f"Descargando... Velocidad: {speed} - ETA: {eta}")
            
        elif d['status'] == 'finished':
            self.root.after(0, self.update_progress, 100)
            self.root.after(0, self.update_status, "Procesando archivo...")
            
    def update_progress(self, percent):
        """Actualiza la barra de progreso"""
        self.progress_var.set(percent)
        
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        
    def download_success(self, video_title):
        """Maneja descarga exitosa"""
        self.set_downloading_state(False)
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, self.placeholder_text)
        self.url_entry.config(fg='#999999')
        self.status_label.config(text="¡Descarga completada!", fg="#00AA00")
        
        messagebox.showinfo(
            "¡Éxito!", 
            f"El video '{video_title}' se ha descargado correctamente.\n\n"
            f"Ubicación: {self.download_path}"
        )
        
    def download_error(self, error_msg):
        """Maneja errores de descarga"""
        self.set_downloading_state(False)
        self.status_label.config(text="Error en la descarga", fg="#FF0000")
        
        if "Video unavailable" in error_msg:
            user_msg = "El video no está disponible. Puede estar privado o haber sido eliminado."
        elif "network" in error_msg.lower():
            user_msg = "Error de conexión. Verifica tu conexión a internet."
        else:
            user_msg = "Ha ocurrido un error durante la descarga."
            
        messagebox.showerror("Error", user_msg)
        
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


def main():
    """Función principal"""
    app = YouTubeDownloader()
    app.run()


if __name__ == "__main__":
    main()
