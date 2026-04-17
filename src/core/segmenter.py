import cv2
import numpy as np
from PIL import Image
import os
from scipy.signal import find_peaks


def segment_lines(image_bytes, debug=True):
    # ... setup debug as before ...

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # 1. Binarize and use very aggressive horizontal dilation
    # We want to turn words into "bars" so we can see the row density clearly
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # 2. Calculate the "Ink Profile" (Horizontal Projection)
    projection = np.sum(dilated, axis=1)

    # 3. Smooth the profile to remove "jitter" from single overlapping letters
    # This helps find the "valleys" between the dense line centers
    smoothed = np.convolve(projection, np.ones(20) / 20, mode='same')

    # 4. Find "Valleys" (Cut Points)
    # We look for points where the ink density is significantly lower
    # than the peaks on either side.
    # We invert the signal to find valleys as "peaks"
    valleys, _ = find_peaks(-smoothed, distance=40)  # distance = approx line height

    lines = []
    prev_y = 0
    for y in valleys:
        # Each valley is our "best guess" for a cut point,
        # even if a few pixels of ink are being sliced through.
        line_crop = img[prev_y:y, :]

        # Only keep if there is actually ink in this crop
        if np.sum(thresh[prev_y:y, :]) > 5000:
            lines.append(Image.fromarray(line_crop).convert("RGB"))
            if debug:
                lines[-1].save(f"data/debug/line_{len(lines):03d}.png")
        prev_y = y

    # Add the final chunk
    if height - prev_y > 20:
        lines.append(Image.fromarray(img[prev_y:, :]).convert("RGB"))

    return lines
