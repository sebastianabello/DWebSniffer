# utils/hashing.py

import hashlib
from pathlib import Path

def calculate_hash(content: str) -> str:
    """
    Calcula el hash SHA256 del contenido HTML.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def has_changed(domain: str, new_hash: str, hash_file: Path) -> bool:
    """
    Compara el hash actual con el anterior y guarda el nuevo si cambió.
    """
    old_hash = None

    if hash_file.exists():
        with open(hash_file, "r") as f:
            old_hash = f.read().strip()

    changed = (old_hash != new_hash)

    with open(hash_file, "w") as f:
        f.write(new_hash)

    if changed:
        print(f"[CAMBIO] Detectado cambio en {domain}")
    else:
        print(f"[SIN CAMBIO] {domain} no cambió")

    return changed
