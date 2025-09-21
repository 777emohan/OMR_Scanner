import cv2
import numpy as np
from typing import Tuple, Optional

def preprocess_image(img_path: str) -> np.ndarray:
    """
    Preprocess OMR sheet image for bubble detection.
    
    Args:
        img_path: Path to the input image
        
    Returns:
        Preprocessed grayscale image with corrected perspective
    """
    # Read image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not load image from {img_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Find contours to detect sheet edges
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return gray
    
    # Find the largest contour (assuming it's the sheet)
    sheet_contour = max(contours, key=cv2.contourArea)
    
    # Approximate the contour to get corners
    peri = cv2.arcLength(sheet_contour, True)
    approx = cv2.approxPolyDP(sheet_contour, 0.02 * peri, True)
    
    # If we found 4 corners, correct perspective
    if len(approx) == 4:
        # Get corner points
        pts = np.float32([pt[0] for pt in approx])
        
        # Define destination rectangle (standardized size)
        rect = np.array([[0, 0], [800, 0], [800, 1000], [0, 1000]], dtype="float32")
        
        # Calculate perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts, rect)
        
        # Apply perspective correction
        warped = cv2.warpPerspective(gray, matrix, (800, 1000))
        return warped
    
    return gray

def detect_sheet_orientation(img: np.ndarray) -> str:
    """
    Detect if the sheet is in portrait or landscape orientation.
    
    Args:
        img: Preprocessed image
        
    Returns:
        'portrait' or 'landscape'
    """
    h, w = img.shape
    return 'portrait' if h > w else 'landscape'

def enhance_contrast(img: np.ndarray) -> np.ndarray:
    """
    Enhance contrast of the image for better bubble detection.
    
    Args:
        img: Input grayscale image
        
    Returns:
        Contrast-enhanced image
    """
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(img)
    return enhanced

def remove_noise(img: np.ndarray) -> np.ndarray:
    """
    Remove noise from the image using morphological operations.
    
    Args:
        img: Input binary image
        
    Returns:
        Denoised image
    """
    # Define kernel for morphological operations
    kernel = np.ones((3, 3), np.uint8)
    
    # Remove small noise
    cleaned = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    
    # Fill small holes
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    
    return cleaned
