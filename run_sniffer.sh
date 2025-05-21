#!/bin/bash

# la ruta de tu proyecto
cd /home/

# Activar entorno virtual
source venv/bin/activate

# Ejecutar el script principal
/usr/bin/python3 main.py >> logs/cron.log 2>&1
