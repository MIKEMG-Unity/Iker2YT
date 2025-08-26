"""
Script de prueba para verificar la funcionalidad básica
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Prueba que todas las importaciones funcionen"""
    try:
        import tkinter as tk
        print("✅ tkinter OK")
        
        import yt_dlp
        print("✅ yt-dlp OK")
        
        import threading
        print("✅ threading OK")
        
        from pathlib import Path
        print("✅ pathlib OK")
        
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_yt_dlp_basic():
    """Prueba básica de yt-dlp sin descargar"""
    try:
        import yt_dlp
        
        # URL de prueba (video público de YouTube)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            if info and 'title' in info:
                print("✅ yt-dlp puede extraer información correctamente")
                return True
            else:
                print("❌ yt-dlp no pudo extraer información")
                return False
                
    except Exception as e:
        print(f"❌ Error en yt-dlp: {e}")
        return False

def test_gui_creation():
    """Prueba que se puede crear la interfaz gráfica"""
    try:
        import tkinter as tk
        
        root = tk.Tk()
        root.title("Test")
        root.withdraw()  # Ocultar ventana de prueba
        
        # Probar widgets básicos
        label = tk.Label(root, text="Test")
        entry = tk.Entry(root)
        button = tk.Button(root, text="Test")
        
        root.destroy()
        print("✅ Interfaz gráfica se puede crear correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con interfaz gráfica: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🧪 Ejecutando pruebas de Iker2YT")
    print("=" * 40)
    
    tests = [
        ("Importaciones", test_imports),
        ("Interfaz gráfica", test_gui_creation),
        ("yt-dlp básico", test_yt_dlp_basic),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Probando: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ Falló: {test_name}")
    
    print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista.")
        return 0
    else:
        print("❌ Algunas pruebas fallaron. Revisa la configuración.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
