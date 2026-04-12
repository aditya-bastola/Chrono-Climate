import cv2
import numpy as np


def process_water_image(image_path):
    """Process a satellite image, isolate water pixels via HSV thresholding,
    and return the pixel count plus a neon-blue segmentation overlay."""

    img = cv2.imread(image_path)
    if img is None:
        return (0, None)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # HSV range targeting blue/dark water — may need tuning per dataset
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    water_pixel_count = int(cv2.countNonZero(mask))

    segmented = img.copy()
    segmented[mask > 0] = [255, 200, 0]  # neon blue in BGR
    segmented_rgb = cv2.cvtColor(segmented, cv2.COLOR_BGR2RGB)

    return (water_pixel_count, segmented_rgb)
