from pathlib import Path
from datetime import datetime

# Directorios
DATA_DIR = Path("data")
LOG_DIR = Path("logs")

# Fecha actual (para carpetas)
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M")

# User-Agent headers
HEADERS = {
    "desktop": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
    },
    "mobile": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; ...)"
    }
}

# Correo
EMAIL_SENDER = "@gmail.com"
EMAIL_RECEIVER = "@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = ""

# Timeout de requests
REQUEST_TIMEOUT = 10
