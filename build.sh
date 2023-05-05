#!/bin/bash

# Crear un entorno virtual y activarlo
python -m venv myenv
source myenv/bin/activate

# Instalar cualquier dependencia que tu proyecto necesite
pip install numpy # ejemplo de dependencia

# No es necesario ejecutar comandos para compilar tu proyecto en Python