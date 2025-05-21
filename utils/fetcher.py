import requests
from config import HEADERS, REQUEST_TIMEOUT
from pathlib import Path

def is_accessible(url):
    """
    Verifica si el dominio es accesible con un HEAD o GET request.
    """
    try:
        response = requests.get(url, headers=HEADERS["desktop"], timeout=REQUEST_TIMEOUT)
        return response.status_code in [200, 301, 302]
    except Exception as e:
        print(f"Error al verificar {url}: {e}")
        return False

def download_site(url, save_path: Path):
    """
    Descarga el contenido HTML del sitio (sin JS) y lo guarda.
    """
    try:
        response = requests.get(url, headers=HEADERS["desktop"], timeout=REQUEST_TIMEOUT)
        html = response.text
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return ""
