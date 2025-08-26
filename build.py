"""
Script de construcción para crear el ejecutable de Iker2YT
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build():
    """Limpia directorios de construcción anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Limpiado: {dir_name}")


def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import yt_dlp
        import tkinter
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False


def build_executable():
    """Construye el ejecutable con PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    # Encontrar el ejecutable de PyInstaller en el entorno virtual
    pyinstaller_path = "pyinstaller"
    if os.path.exists(".venv"):
        if sys.platform == "win32":
            venv_pyinstaller = ".venv/Scripts/pyinstaller.exe"
        else:
            venv_pyinstaller = ".venv/bin/pyinstaller"
        
        if os.path.exists(venv_pyinstaller):
            pyinstaller_path = venv_pyinstaller
    
    # Configuración de PyInstaller
    cmd = [
        pyinstaller_path,
        "--onefile",                    # Un solo archivo
        "--windowed",                   # Sin consola (para Windows)
        "--name=Iker2YT",              # Nombre del ejecutable
        "--distpath=dist",              # Directorio de salida
        "--workpath=build",             # Directorio de trabajo
        "--clean",                      # Limpiar cache
        "src/downloader.py"             # Archivo principal
    ]
    
    # Agregar icono solo si existe
    if os.path.exists("assets/icon.ico"):
        cmd.extend(["--icon=assets/icon.ico"])
        # Incluir assets
        if sys.platform == "darwin":
            cmd.extend(["--add-data=assets:assets"])
        else:
            cmd.extend(["--add-data=assets;assets"])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Ejecutable creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear ejecutable: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ No se encontró PyInstaller en: {pyinstaller_path}")
        print("💡 Asegúrate de que PyInstaller esté instalado: pip install pyinstaller")
        return False


def create_release_package():
    """Crea un paquete de distribución"""
    if not os.path.exists("dist/Iker2YT"):
        if sys.platform == "win32":
            executable_name = "Iker2YT.exe"
        else:
            executable_name = "Iker2YT"
            
        if not os.path.exists(f"dist/{executable_name}"):
            print("❌ No se encontró el ejecutable")
            return False
    
    print("📦 Creando paquete de distribución...")
    
    # Crear directorio de release
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copiar ejecutable
    if sys.platform == "win32":
        shutil.copy("dist/Iker2YT.exe", f"{release_dir}/Iker2YT.exe")
    else:
        shutil.copy("dist/Iker2YT", f"{release_dir}/Iker2YT")
    
    # Crear README para usuario final
    readme_content = """# Iker2YT - Descargador de YouTube

## 🚀 Cómo usar

1. Haz doble clic en el archivo Iker2YT.exe
2. Pega la URL del video de YouTube que quieres descargar
3. (Opcional) Cambia la carpeta de destino
4. (Opcional) Selecciona la calidad deseada
5. Haz clic en "Descargar Video"
6. ¡Disfruta tu video!

## 📝 Notas

- Los videos se guardan por defecto en tu carpeta de Descargas
- Puedes descargar solo el audio seleccionando "Solo audio (MP3)"
- La aplicación funciona sin conexión una vez descargada
- No requiere instalación adicional

## ⚠️ Importante

- Respeta los derechos de autor
- Usa solo para contenido del que tengas permisos
- Algunos videos pueden estar restringidos geográficamente

## 🆘 ¿Problemas?

Si tienes algún problema:
1. Verifica que la URL sea de YouTube
2. Comprueba tu conexión a internet
3. Intenta con otro video

¡Gracias por usar Iker2YT! 🎬
"""
    
    with open(f"{release_dir}/LEEME.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ Paquete creado en: {release_dir}/")
    return True


def main():
    """Función principal del script de construcción"""
    print("🏗️  Iker2YT Builder")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("src/downloader.py"):
        print("❌ No se encontró src/downloader.py")
        print("💡 Ejecuta este script desde la raíz del proyecto")
        return 1
    
    # Paso 1: Limpiar construcciones anteriores
    clean_build()
    
    # Paso 2: Verificar dependencias
    if not check_dependencies():
        return 1
    
    # Paso 3: Construir ejecutable
    if not build_executable():
        return 1
    
    # Paso 4: Crear paquete de distribución
    if not create_release_package():
        return 1
    
    print("\n🎉 ¡Construcción completada!")
    print("📁 El ejecutable está en: dist/")
    print("📦 El paquete de distribución está en: release/")
    print("\n💡 Ahora puedes compartir la carpeta 'release' con tu amigo")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
