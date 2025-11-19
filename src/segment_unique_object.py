"""
for each image → find the stone, make a mask, get a box and outline
"""
import cv2
import numpy as np

def segment_unique_object(img_path):
    """
    Segment the unique object in the image, assuming a single object on a black background.
    """
    img_bgr = cv2.imread(img_path)

    # 1) Work on a copy so we never touch the original
    work = img_bgr.copy()

    # 2) To gray + slight blur
    gray = cv2.cvtColor(work, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    

    # 3) Otsu threshold to roughly separate foreground from black background
    otsu_t, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Sometimes Otsu is a bit high because of bright labels.
    # Using a fraction of it works well for dark stones.
    t = max(5, int(otsu_t * 0.5))
    _, fg = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)

    # 4) Morphological clean-up (close small gaps, remove tiny specks)
    kernel_close = np.ones((7, 7), np.uint8)
    kernel_open = np.ones((3, 3), np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel_close)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel_open)
    
    # 5) Find contours, keep biggest one (the stone)
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        # No object found – return empty mask + bbox
        return np.zeros_like(gray), (0, 0, 0, 0)
    main_cnt = max(cnts, key=cv2.contourArea)
    
    # 6) Draw mask
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [main_cnt], -1, 255, thickness=cv2.FILLED)
    
    # 7) Axis-aligned bounding box
    x, y, w_box, h_box = cv2.boundingRect(main_cnt)
    bbox = (x, y, w_box, h_box)
    return mask, bbox


