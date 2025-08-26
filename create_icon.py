"""
Script para crear un icono básico para Iker2YT
Genera un icono temporal hasta que tengas uno personalizado
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_icon():
    """Crea un icono simple para la aplicación"""
    # Crear imagen de 256x256
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fondo circular con gradiente
    for i in range(size//2):
        alpha = int(255 * (1 - i/(size//2)))
        color = (220, 53, 69, alpha)  # Rojo YouTube con transparencia
        draw.ellipse([i, i, size-i, size-i], fill=color)
    
    # Triángulo de play (símbolo de YouTube)
    triangle_size = size // 3
    center_x, center_y = size // 2, size // 2
    
    # Puntos del triángulo
    points = [
        (center_x - triangle_size//2, center_y - triangle_size//2),
        (center_x - triangle_size//2, center_y + triangle_size//2),
        (center_x + triangle_size//2, center_y)
    ]
    
    draw.polygon(points, fill=(255, 255, 255, 255))
    
    # Guardar en múltiples tamaños para mejor compatibilidad
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Guardar como ICO
    icon_path = os.path.join('assets', 'icon.ico')
    images[0].save(icon_path, format='ICO', sizes=[(s, s) for s in sizes])
    
    print(f"✅ Icono creado: {icon_path}")
    
    # También crear PNG para preview
    img.save(os.path.join('assets', 'icon_preview.png'), format='PNG')
    print(f"✅ Preview PNG creado: assets/icon_preview.png")

if __name__ == "__main__":
    try:
        create_simple_icon()
    except ImportError:
        print("❌ Pillow no está instalado. Instalando...")
        import subprocess
        subprocess.run(["pip", "install", "Pillow"], check=True)
        create_simple_icon()
    except Exception as e:
        print(f"❌ Error creando icono: {e}")
        print("💡 Puedes crear un icono manualmente y guardarlo como assets/icon.ico")
