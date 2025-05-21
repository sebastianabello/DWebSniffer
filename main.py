import os
from datetime import datetime
from config import DATA_DIR, TIMESTAMP
from utils.fetcher import is_accessible, download_site
from utils.notifier import EmailNotifier
from utils.screenshot import capture_screenshot
from utils.hashing import calculate_hash, has_changed
from utils.comparator import highlight_differences
from pathlib import Path


def load_domains(file_path="domains.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def get_latest_previous_screenshot(domain_clean: str, current_timestamp: str) -> Path | None:
    """
    Busca el último screenshot anterior (por timestamp completo) para el dominio.
    """
    domain_path = DATA_DIR / domain_clean
    if not domain_path.exists():
        return None

    try:
        current_ts = datetime.strptime(current_timestamp, "%Y-%m-%d_%H%M")
    except ValueError:
        print(f"❌ Formato de timestamp inválido: {current_timestamp}")
        return None

    previous = []
    for folder in domain_path.iterdir():
        if folder.is_dir() and "_" in folder.name:
            try:
                folder_ts = datetime.strptime(folder.name, "%Y-%m-%d_%H%M")
                if folder_ts < current_ts:
                    previous.append((folder_ts, folder))
            except ValueError:
                continue

    if not previous:
        return None

    previous.sort(reverse=True)
    latest_folder = previous[0][1]
    screenshot_path = latest_folder / "screenshot.png"

    return screenshot_path if screenshot_path.exists() else None


def process_domain(domain):
    print(f"\n🟡 Procesando {domain}...")

    if not is_accessible(domain):
        print(f"🔴 No accesible: {domain}")
        return None

    domain_clean = domain.replace("https://", "").replace("http://", "").replace("/", "_")
    domain_path = DATA_DIR / domain_clean
    os.makedirs(domain_path, exist_ok=True) 
    html_path = domain_path / "page.html"
    hash_path = domain_path / "hash.txt"

    # Descargar HTML
    html_content = download_site(domain, html_path)

    # Calcular hash
    current_hash = calculate_hash(html_content)
    changed = has_changed(domain, current_hash, hash_path)

    if not changed:
        print("🟢 No hay cambios en hash, omitiendo screenshot y carpeta.")
        return None

    # Guardar nuevo HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Crear carpeta solo si hubo cambios
    domain_folder = domain_path / TIMESTAMP
    os.makedirs(domain_folder, exist_ok=True)
    screenshot_path = domain_folder / "screenshot.png"
    diff_output = domain_folder / "diff.png"

    # Captura y comparación
    capture_screenshot(domain, screenshot_path)
    prev_screenshot_path = get_latest_previous_screenshot(domain_clean, TIMESTAMP)

    if prev_screenshot_path:
        highlight_differences(prev_screenshot_path, screenshot_path, diff_output)
    else:
        print("⚠️ No se encontró screenshot anterior para comparar.")

    return domain


if __name__ == "__main__":
    domains = load_domains()
    changed_domains = []

    for domain in domains:
        result = process_domain(domain)
        if result:
            changed_domains.append(result)

    if changed_domains:
        print("\n✅ Cambios detectados en los siguientes dominios:")
        for d in changed_domains:
            print(f" - {d}")

        EmailNotifier().send(changed_domains)
    else:
        print("\n🟢 No se detectaron cambios.")
