import cv2
import numpy as np
from typing import List, Tuple, Dict
import math

def extract_bubbles(sheet_img: np.ndarray, rows: int = 20, cols: int = 5, 
                   bubble_size: Tuple[int, int] = (40, 40)) -> List[List[int]]:
    """
    Extract bubble markings from the OMR sheet.
    
    Args:
        sheet_img: Preprocessed sheet image
        rows: Number of rows (questions)
        cols: Number of columns (subjects/options)
        bubble_size: Expected size of each bubble (width, height)
        
    Returns:
        2D list where each element is 1 if bubble is filled, 0 otherwise
    """
    h, w = sheet_img.shape
    bubble_h = h // rows
    bubble_w = w // cols
    
    bubbles = []
    
    for i in range(rows):
        row = []
        for j in range(cols):
            # Calculate bubble region coordinates
            y1 = i * bubble_h
            y2 = min((i + 1) * bubble_h, h)
            x1 = j * bubble_w
            x2 = min((j + 1) * bubble_w, w)
            
            # Extract bubble region
            bubble_region = sheet_img[y1:y2, x1:x2]
            
            # Calculate fill ratio
            fill_ratio = cv2.countNonZero(bubble_region) / (bubble_region.size)
            
            # Threshold for determining if bubble is filled
            # Adjust threshold based on bubble size and image quality
            threshold = 0.3 if bubble_region.size > 100 else 0.5
            
            row.append(1 if fill_ratio > threshold else 0)
        
        bubbles.append(row)
    
    return bubbles

def detect_bubbles_advanced(sheet_img: np.ndarray, rows: int = 20, cols: int = 5) -> List[List[Dict]]:
    """
    Advanced bubble detection with more detailed information.
    
    Args:
        sheet_img: Preprocessed sheet image
        rows: Number of rows (questions)
        cols: Number of columns (subjects/options)
        
    Returns:
        2D list of dictionaries containing bubble information
    """
    h, w = sheet_img.shape
    bubble_h = h // rows
    bubble_w = w // cols
    
    bubbles = []
    
    for i in range(rows):
        row = []
        for j in range(cols):
            # Calculate bubble region coordinates
            y1 = i * bubble_h
            y2 = min((i + 1) * bubble_h, h)
            x1 = j * bubble_w
            x2 = min((j + 1) * bubble_w, w)
            
            # Extract bubble region
            bubble_region = sheet_img[y1:y2, x1:x2]
            
            # Calculate various metrics
            fill_ratio = cv2.countNonZero(bubble_region) / (bubble_region.size)
            mean_intensity = np.mean(bubble_region)
            std_intensity = np.std(bubble_region)
            
            # Detect circular shape (bubbles should be roughly circular)
            contours, _ = cv2.findContours(bubble_region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            circularity = 0
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)
                if perimeter > 0:
                    circularity = 4 * math.pi * area / (perimeter * perimeter)
            
            # Determine if bubble is filled
            is_filled = fill_ratio > 0.3 and circularity > 0.3
            
            bubble_info = {
                'filled': 1 if is_filled else 0,
                'fill_ratio': fill_ratio,
                'mean_intensity': mean_intensity,
                'std_intensity': std_intensity,
                'circularity': circularity,
                'coordinates': (x1, y1, x2, y2)
            }
            
            row.append(bubble_info)
        
        bubbles.append(row)
    
    return bubbles

def detect_bubble_grid(sheet_img: np.ndarray) -> Tuple[int, int]:
    """
    Automatically detect the number of rows and columns in the bubble grid.
    
    Args:
        sheet_img: Preprocessed sheet image
        
    Returns:
        Tuple of (rows, cols)
    """
    # Apply edge detection
    edges = cv2.Canny(sheet_img, 50, 150)
    
    # Detect horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    
    horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
    
    # Count lines
    h, w = sheet_img.shape
    rows = len([y for y in range(h) if np.any(horizontal_lines[y, :])])
    cols = len([x for x in range(w) if np.any(vertical_lines[:, x])])
    
    return max(1, rows - 1), max(1, cols - 1)

def validate_bubble_detection(bubbles: List[List[int]], expected_rows: int, expected_cols: int) -> bool:
    """
    Validate that bubble detection results are reasonable.
    
    Args:
        bubbles: Detected bubble markings
        expected_rows: Expected number of rows
        expected_cols: Expected number of columns
        
    Returns:
        True if detection is valid, False otherwise
    """
    if len(bubbles) != expected_rows:
        return False
    
    for row in bubbles:
        if len(row) != expected_cols:
            return False
        # Check for multiple selections in a row (should be rare)
        if sum(row) > 1:
            print(f"Warning: Multiple selections detected in row: {row}")
    
    return True

def get_bubble_statistics(bubbles: List[List[int]]) -> Dict:
    """
    Get statistics about the detected bubbles.
    
    Args:
        bubbles: Detected bubble markings
        
    Returns:
        Dictionary containing statistics
    """
    total_bubbles = sum(len(row) for row in bubbles)
    filled_bubbles = sum(sum(row) for row in bubbles)
    fill_rate = filled_bubbles / total_bubbles if total_bubbles > 0 else 0
    
    # Count multiple selections per row
    multiple_selections = sum(1 for row in bubbles if sum(row) > 1)
    
    return {
        'total_bubbles': total_bubbles,
        'filled_bubbles': filled_bubbles,
        'fill_rate': fill_rate,
        'multiple_selections': multiple_selections,
        'rows': len(bubbles),
        'cols': len(bubbles[0]) if bubbles else 0
    }
