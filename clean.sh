#!/bin/bash

# Colores para los mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando limpieza del proyecto...${NC}"

# Eliminar archivos de caché de Python
echo -e "${GREEN}Eliminando archivos de caché Python...${NC}"
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.pyd" -delete

# Eliminar archivos de cobertura
echo -e "${GREEN}Eliminando archivos de cobertura...${NC}"
rm -rf htmlcov/
rm -f .coverage
rm -f coverage.xml

# Eliminar archivos temporales de pytest
echo -e "${GREEN}Eliminando archivos temporales de pytest...${NC}"
rm -rf .pytest_cache/

# Eliminar archivos de LocalStack
echo -e "${GREEN}Eliminando archivos de LocalStack...${NC}"
rm -rf volume/
rm -rf .localstack/

# Eliminar build de SAM
echo -e "${GREEN}Eliminando build de SAM...${NC}"
rm -rf .aws-sam/

# Eliminar archivos temporales del sistema
echo -e "${GREEN}Eliminando archivos temporales del sistema...${NC}"
find . -type f -name "*.log" -delete
find . -type f -name "*.tmp" -delete
find . -type f -name "*.temp" -delete
find . -type f -name ".DS_Store" -delete

# Eliminar directorios vacíos
echo -e "${GREEN}Eliminando directorios vacíos...${NC}"
find . -type d -empty -delete

echo -e "${YELLOW}Limpieza completada!${NC}"

# Mostrar estadísticas de espacio liberado (solo en sistemas Unix/Linux)
if [ "$(uname)" != "Windows_NT" ]; then
    echo -e "${GREEN}Espacio en disco actual:${NC}"
    df -h .
fi 