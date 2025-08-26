#!/bin/bash

# Script de desarrollo para macOS/Linux
# Facilita las tareas comunes de desarrollo

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iker2YT - Script de Desarrollo${NC}"
echo "================================="

# Función para mostrar ayuda
show_help() {
    echo "Uso: ./dev.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  setup     - Configura el entorno de desarrollo"
    echo "  test      - Ejecuta las pruebas"
    echo "  run       - Ejecuta la aplicación en modo desarrollo"
    echo "  build     - Construye el ejecutable"
    echo "  clean     - Limpia archivos temporales"
    echo "  help      - Muestra esta ayuda"
}

# Configurar entorno
setup_env() {
    echo -e "${YELLOW}📦 Configurando entorno...${NC}"
    
    # Crear entorno virtual si no existe
    if [ ! -d ".venv" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv .venv
    fi
    
    # Activar entorno virtual
    source .venv/bin/activate
    
    # Instalar dependencias
    echo "Instalando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✅ Entorno configurado correctamente${NC}"
}

# Ejecutar pruebas
run_tests() {
    echo -e "${YELLOW}🧪 Ejecutando pruebas...${NC}"
    source .venv/bin/activate
    python test.py
}

# Ejecutar aplicación
run_app() {
    echo -e "${YELLOW}🏃 Ejecutando aplicación...${NC}"
    source .venv/bin/activate
    python src/downloader.py
}

# Construir ejecutable
build_app() {
    echo -e "${YELLOW}🔨 Construyendo ejecutable...${NC}"
    source .venv/bin/activate
    python build.py
}

# Limpiar archivos temporales
clean_files() {
    echo -e "${YELLOW}🧹 Limpiando archivos temporales...${NC}"
    
    # Limpiar directorios de Python
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Limpiar directorios de construcción
    rm -rf build/ 2>/dev/null || true
    rm -rf dist/ 2>/dev/null || true
    rm -rf release/ 2>/dev/null || true
    rm -rf *.spec 2>/dev/null || true
    
    echo -e "${GREEN}✅ Limpieza completada${NC}"
}

# Procesar argumentos
case "${1:-help}" in
    "setup")
        setup_env
        ;;
    "test")
        run_tests
        ;;
    "run")
        run_app
        ;;
    "build")
        build_app
        ;;
    "clean")
        clean_files
        ;;
    "help"|*)
        show_help
        ;;
esac
