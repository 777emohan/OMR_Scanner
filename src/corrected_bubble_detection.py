
import cv2
import numpy as np

def extract_bubbles_corrected(sheet_img, rows=20, cols=5):
    """
    Corrected bubble detection that properly identifies filled vs empty bubbles.
    """
    h, w = sheet_img.shape
    bubble_h = h // rows
    bubble_w = w // cols
    
    # Apply Gaussian blur to smooth the image
    blurred = cv2.GaussianBlur(sheet_img, (5, 5), 0)
    
    # Use adaptive threshold to get better separation
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    bubbles = []
    
    for i in range(rows):
        row = []
        for j in range(cols):
            # Calculate bubble region with padding to avoid edges
            y1 = max(0, i * bubble_h + bubble_h // 4)
            y2 = min(h, (i + 1) * bubble_h - bubble_h // 4)
            x1 = max(0, j * bubble_w + bubble_w // 4)
            x2 = min(w, (j + 1) * bubble_w - bubble_w // 4)
            
            # Extract bubble region
            bubble_region = thresh[y1:y2, x1:x2]
            
            if bubble_region.size == 0:
                row.append(0)
                continue
            
            # Calculate fill ratio
            fill_ratio = cv2.countNonZero(bubble_region) / (bubble_region.size)
            
            # Use higher threshold - bubbles should be mostly dark when filled
            threshold = 0.3
            is_filled = fill_ratio > threshold
            
            row.append(1 if is_filled else 0)
        
        bubbles.append(row)
    
    return bubbles
