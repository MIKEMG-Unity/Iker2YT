# Guía de Desarrollo - Iker2YT

## 🛠️ Configuración del Entorno de Desarrollo

### Requisitos Previos
- Python 3.7 o superior
- Git
- Sistema operativo: Windows, macOS, o Linux

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repo>
   cd Iker2YT
   ```

2. **Configurar entorno (Automático):**
   ```bash
   ./dev.sh setup
   ```
   
   **O manualmente:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🏗️ Estructura del Proyecto

```
Iker2YT/
├── src/
│   └── downloader.py       # Aplicación principal
├── assets/
│   └── icon.ico            # Icono de la aplicación
├── build.py               # Script de construcción
├── dev.sh                 # Script de desarrollo (Unix)
├── test.py                # Pruebas automatizadas
├── requirements.txt       # Dependencias Python
└── README.md             # Documentación usuario final
```

## 🚀 Comandos de Desarrollo

### Usando el script de desarrollo (Recomendado):
```bash
./dev.sh run     # Ejecutar en modo desarrollo
./dev.sh test    # Ejecutar pruebas
./dev.sh build   # Construir ejecutable
./dev.sh clean   # Limpiar archivos temporales
```

### Comandos manuales:
```bash
# Ejecutar aplicación
python src/downloader.py

# Ejecutar pruebas
python test.py

# Construir ejecutable
python build.py
```

## 🧪 Pruebas

El proyecto incluye pruebas automatizadas que verifican:
- ✅ Importaciones de dependencias
- ✅ Creación de interfaz gráfica
- ✅ Funcionalidad básica de yt-dlp

Ejecutar: `./dev.sh test` o `python test.py`

## 📦 Construcción del Ejecutable

### Proceso Automatizado:
```bash
./dev.sh build
```

### Proceso Manual:
```bash
python build.py
```

Esto genera:
- `dist/Iker2YT.exe` (Windows) o `dist/Iker2YT` (macOS/Linux)
- `release/` - Paquete listo para distribución

## 🔧 Configuración Avanzada

### Personalizar PyInstaller

Edita `build.py` para modificar:
- Icono de la aplicación
- Archivos adicionales a incluir
- Opciones de compilación

### Formatos de Video Soportados

El proyecto usa `yt-dlp` que soporta:
- MP4 (video)
- MP3 (solo audio)
- Calidades: Mejor disponible, 720p, 480p

## 🐛 Debugging

### Problemas Comunes:

1. **Error SSL en macOS:**
   ```bash
   pip install --upgrade certifi
   ```

2. **Error de tkinter:**
   - En Ubuntu: `sudo apt-get install python3-tk`
   - En macOS: Viene con Python

3. **yt-dlp no funciona:**
   ```bash
   pip install --upgrade yt-dlp
   ```

### Logs y Diagnóstico:

Para debugging, modifica `src/downloader.py`:
```python
# Habilitar logs detallados
ydl_opts = {
    'verbose': True,  # Agregar esta línea
    # ... otras opciones
}
```

## 🚢 Despliegue

### Para Usuarios Finales:
1. Ejecutar `./dev.sh build`
2. Compartir la carpeta `release/`
3. El usuario solo necesita ejecutar el archivo

### Para Desarrolladores:
1. Documentar cambios en README.md
2. Actualizar requirements.txt si es necesario
3. Probar en diferentes SO antes del release

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Estándares de Código:
- Usar type hints donde sea posible
- Comentarios en español para funciones públicas
- Seguir PEP 8 para estilo de código
- Probar cambios antes de commit

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.
