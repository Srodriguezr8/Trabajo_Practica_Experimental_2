#!/bin/bash
# ---------------------------------------------
# Script avanzado para configurar y ejecutar Django
# Linux / macOS
# ---------------------------------------------

# Colores
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m" # Sin color

echo -e "${GREEN}========================================="
echo "  CONFIGURACION Y EJECUCION DE DJANGO"
echo "=========================================${NC}"
echo

# --------------------------
# 1. Verificar Python
# --------------------------
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}ERROR: Python3 no está instalado o no está en PATH.${NC}"
    exit 1
fi
echo -e "${GREEN}Python detectado correctamente.${NC}"
python3 --version
echo

# --------------------------
# 2. Crear entorno virtual
# --------------------------
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo crear el entorno virtual.${NC}"
        exit 1
    fi
else
    echo "Entorno virtual ya existe."
fi
echo

# --------------------------
# 3. Activar entorno virtual
# --------------------------
echo "Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo activar el entorno virtual.${NC}"
    exit 1
fi
echo -e "${GREEN}Entorno virtual activo.${NC}"
echo

# --------------------------
# 4. Instalar dependencias
# --------------------------
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt no encontrado."
    echo "Instalando Django 5.2.2 por defecto..."
    pip install django==5.2.2
fi
echo

# --------------------------
# 5. Aplicar migraciones
# --------------------------
echo "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Fallo al aplicar migraciones.${NC}"
    exit 1
fi
echo -e "${GREEN}Migraciones aplicadas correctamente.${NC}"
echo

# --------------------------
# 6. Ejecutar servidor
# --------------------------
echo -e "${YELLOW}Levantando servidor de desarrollo en http://127.0.0.1:8000/"
echo "Presiona CTRL+C para detener el servidor."
python manage.py runserver
