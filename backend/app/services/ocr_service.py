import cv2
import numpy as np
import pytesseract
import logging
from typing import Dict, List, Any, Optional
from PIL import Image
import io
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    """
    OCR service for extracting text and error codes from images
    """
    
    def __init__(self, tesseract_cmd_path: Optional[str] = None):
        """
        Initialize the OCR service
        
        Args:
            tesseract_cmd_path (str, optional): Path to tesseract executable. 
                If not provided, will try to auto-detect.
        """
        self.tesseract_cmd_path = tesseract_cmd_path
        self._setup_tesseract()
    
    def _setup_tesseract(self):
        """Setup tesseract path"""
        if self.tesseract_cmd_path and os.path.exists(self.tesseract_cmd_path):
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd_path
            logger.info(f"Tesseract configured at: {self.tesseract_cmd_path}")
            return
        
        # Try to auto-detect tesseract
        try:
            # For Windows
            if os.name == 'nt':
                possible_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                    r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
                ]
            # For Linux/Mac
            else:
                possible_paths = [
                    "/usr/bin/tesseract",
                    "/usr/local/bin/tesseract",
                    "/opt/homebrew/bin/tesseract",
                ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"Tesseract found at: {path}")
                    self.tesseract_cmd_path = path
                    break
            else:
                logger.warning("Tesseract not found in common locations. Please install Tesseract-OCR.")
        except Exception as e:
            logger.warning(f"Could not configure Tesseract path: {e}")
    
    def process_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Process image data to extract text and error codes
        
        Args:
            image_data (bytes): Raw image data
            
        Returns:
            dict: Extracted text and error codes
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess the image
            processed_image = self._preprocess_image(opencv_image)
            
            # Extract text using OCR
            extracted_text = self._extract_text(processed_image)
            
            # Extract error codes from the text
            error_codes = self._extract_error_codes(extracted_text)
            
            return {
                "extracted_text": extracted_text,
                "error_codes": error_codes,
                "success": True
            }
        
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return {
                "extracted_text": "",
                "error_codes": [],
                "success": False,
                "error": str(e)
            }
    
    def _preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Try different thresholding methods
            # Method 1: Otsu's thresholding
            _, thresh_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Method 2: Adaptive thresholding
            thresh_adaptive = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply morphological operations to clean up the image
            kernel = np.ones((1, 1), np.uint8)
            cleaned_otsu = cv2.morphologyEx(thresh_otsu, cv2.MORPH_CLOSE, kernel)
            cleaned_adaptive = cv2.morphologyEx(thresh_adaptive, cv2.MORPH_CLOSE, kernel)
            
            # Return both and let the extract_text method decide which works better
            return {
                "otsu": cleaned_otsu,
                "adaptive": cleaned_adaptive
            }
        
        except Exception as e:
            logger.warning(f"Error in image preprocessing: {e}")
            return {"original": image}
    
    def _extract_text(self, processed_images):
        """Extract text from preprocessed images"""
        best_text = ""
        best_confidence = 0
        
        # Configure OCR parameters
        custom_config = r'--oem 3 --psm 6'
        
        for method, image in processed_images.items():
            try:
                # Extract text with confidence data
                data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
                
                # Calculate average confidence for non-empty text
                confidences = [int(conf) for i, conf in enumerate(data['conf']) 
                              if int(conf) > 0 and data['text'][i].strip()]
                
                if confidences:
                    avg_confidence = sum(confidences) / len(confidences)
                    text = ' '.join([t for t in data['text'] if t.strip()])
                    
                    # Keep the text with highest confidence
                    if avg_confidence > best_confidence:
                        best_confidence = avg_confidence
                        best_text = text
            except Exception as e:
                logger.warning(f"Error extracting text with {method} method: {e}")
                continue
        
        # Clean up the text
        best_text = best_text.strip()
        best_text = re.sub(r'\s+', ' ', best_text)  # Replace multiple spaces with single space
        
        return best_text
    
    def _extract_error_codes(self, text: str) -> List[str]:
        """Extract error codes from text using regex patterns"""
        error_codes = []
        
        if not text:
            return error_codes
        
        # Common error code patterns
        patterns = [
            r'\b(error|exception|fault|failure|alert|warning|code)[\s:]+([A-Za-z0-9\-_]+)\b',
            r'\b([A-Z][0-9]{3,6})\b',  # Common format like E1234, E12345
            r'\b([A-Z]-[0-9]{2,5})\b',  # Format like E-123
            r'\b([A-Z]{2,5}[0-9]{2,5})\b',  # Format like ERR123, ERROR123
            r'\b([A-Z]{2,5}-[0-9]{2,5})\b',  # Format like ERR-123, ERROR-123
            r'\b(0x[0-9A-Fa-f]{2,8})\b',  # Hexadecimal error codes
            r'\b([0-9]{3,6})\b',  # Numeric error codes
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # For patterns with capture groups, take the error code part
                    error_code = match[1] if len(match) > 1 else match[0]
                else:
                    error_code = match
                
                # Filter out very short or common false positives
                if len(error_code) >= 3 and error_code not in ['the', 'and', 'for', 'not']:
                    error_codes.append(error_code.upper())
        
        # Remove duplicates and return
        return sorted(list(set(error_codes)))