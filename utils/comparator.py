from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
from scipy.ndimage import label, find_objects


def highlight_differences(img1_path: Path, img2_path: Path, output_path: Path, threshold: int = 30, min_area: int = 100):
    """
    Compara dos imágenes, detecta diferencias y dibuja múltiples rectángulos rojos sobre regiones cambiadas.
    """
    try:
        img1 = Image.open(img1_path).convert("L")
        img2 = Image.open(img2_path).convert("L")

        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Diferencia absoluta por píxel
        diff = np.abs(arr1.astype("int16") - arr2.astype("int16"))

        # Máscara binaria de cambios
        mask = diff > threshold

        if not np.any(mask):
            print("🟢 No hay diferencias visibles")
            return False

        # Etiquetar regiones conectadas
        labeled_array, num_features = label(mask)
        slices = find_objects(labeled_array)

        # Crear imagen RGB sobre la que dibujar
        result_img = img2.convert("RGB")
        draw = ImageDraw.Draw(result_img)

        for region in slices:
            y1, x1 = region[0].start, region[1].start
            y2, x2 = region[0].stop, region[1].stop

            # Filtrar por tamaño mínimo
            if (x2 - x1) * (y2 - y1) < min_area:
                continue

            # Dibujar rectángulo
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        result_img.save(output_path)
        print(f"🟥 Diferencias múltiples marcadas y guardadas en {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error al comparar imágenes: {e}")
        return False
