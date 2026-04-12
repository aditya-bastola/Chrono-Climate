import cv2
import numpy as np


def process_water_image(image_path):
    """Process a satellite image, isolate water pixels via HSV thresholding,
    and return the pixel count plus a neon-blue segmentation overlay."""

    img = cv2.imread(image_path)
    if img is None:
        return (0, None)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Mask 1: Deep saturated blue (dark lake cores) — may need tuning per dataset
    mask_deep = cv2.inRange(hsv, np.array([85, 25, 25]), np.array([135, 255, 255]))

    # Mask 2: Pale/light blue, cyan, turquoise (shallow edges, sun-bleached surfaces)
    mask_light = cv2.inRange(hsv, np.array([65, 5, 55]), np.array([150, 130, 255]))

    # Mask 3: Neutral/grey tones — cloud haze, moist lakebed, desaturated water.
    mask_grey = cv2.inRange(hsv, np.array([0, 0, 72]), np.array([179, 35, 210]))

    # Exclusion mask: warm brown/orange/tan arid land
    mask_arid = cv2.inRange(hsv, np.array([5, 18, 50]), np.array([35, 255, 220]))

    # Combine water masks then subtract confirmed arid land
    mask_water = cv2.bitwise_or(mask_deep, cv2.bitwise_or(mask_light, mask_grey))
    mask = cv2.bitwise_and(mask_water, cv2.bitwise_not(mask_arid))
    water_pixel_count = int(cv2.countNonZero(mask))

    segmented = img.copy()
    segmented[mask > 0] = [255, 200, 0]  # neon blue in BGR
    segmented_rgb = cv2.cvtColor(segmented, cv2.COLOR_BGR2RGB)

    return (water_pixel_count, segmented_rgb)
