
def extract_bubbles_improved(sheet_img, rows=20, cols=5):
    """
    Improved bubble detection with better thresholding.
    """
    h, w = sheet_img.shape
    bubble_h = h // rows
    bubble_w = w // cols
    
    # Use higher threshold to avoid detecting all bubbles
    _, thresh = cv2.threshold(sheet_img, 200, 255, cv2.THRESH_BINARY_INV)
    
    bubbles = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # Calculate bubble region
            y1 = i * bubble_h
            y2 = min((i + 1) * bubble_h, h)
            x1 = j * bubble_w
            x2 = min((j + 1) * bubble_w, w)
            
            # Extract bubble region
            bubble_region = thresh[y1:y2, x1:x2]
            
            # Calculate fill ratio
            fill_ratio = cv2.countNonZero(bubble_region) / (bubble_region.size)
            
            # Use much lower threshold
            threshold = 0.1
            is_filled = fill_ratio > threshold
            
            row.append(1 if is_filled else 0)
        
        bubbles.append(row)
    
    return bubbles
