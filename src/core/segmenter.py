import cv2
import numpy as np
from PIL import Image


def segment_lines(image_bytes):
    """Slices a high-res page into line strips based on whitespace."""
    # Convert bytes to OpenCV format
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # 1. Binarization (Crucial for 18th-century paper)
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 2. Horizontal Projection
    # Sum pixels horizontally to find gaps between lines
    projection = np.sum(thresh, axis=1)

    # 3. Find line boundaries
    # This is a simple logic: any row with very few black pixels is a gap
    threshold_value = np.max(projection) * 0.05
    line_indices = np.where(projection > threshold_value)[0]

    lines = []
    if len(line_indices) > 0:
        start_idx = line_indices[0]
        for i in range(1, len(line_indices)):
            # If there's a gap of more than 10 pixels, call it a new line
            if line_indices[i] - line_indices[i - 1] > 10:
                end_idx = line_indices[i - 1]
                # Crop the original grayscale image (not the thresholded one)
                line_crop = img[start_idx:end_idx, :]
                lines.append(Image.fromarray(line_crop).convert("RGB"))
                start_idx = line_indices[i]

        # Add the last line
        lines.append(Image.fromarray(img[start_idx:line_indices[-1], :]).convert("RGB"))

    return lines
