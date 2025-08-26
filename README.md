# Iker2YT - Descargador de YouTube

Un descargador de YouTube simple y fácil de usar con interfaz gráfica, creado específicamente para usuarios no técnicos.

## 🎯 Características

- Interfaz gráfica intuitiva
- Descarga en la mejor calidad disponible
- Un solo archivo ejecutable (.exe)
- No requiere instalación
- Funciona offline

## 🚀 Uso

1. Ejecuta `descargador.exe`
2. Pega la URL del video de YouTube
3. Haz clic en "Descargar"
4. El video se guardará en la misma carpeta

## 🛠️ Desarrollo

### Requisitos
- Python 3.7+
- yt-dlp
- tkinter (incluido con Python)
- PyInstaller

### Instalación para desarrollo
```bash
pip install -r requirements.txt
```

### Ejecutar en modo desarrollo
```bash
python src/downloader.py
```

### Crear ejecutable
```bash
python build.py
```

## 📁 Estructura del proyecto
```
Iker2YT/
├── src/
│   └── downloader.py       # Código principal
├── assets/
│   └── icon.ico            # Icono de la aplicación
├── dist/                   # Ejecutables generados
├── requirements.txt        # Dependencias
├── build.py               # Script de construcción
└── README.md
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - ve el archivo LICENSE para más detalles.
