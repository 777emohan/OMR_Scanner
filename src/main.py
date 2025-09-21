import os
import sys
import argparse
from typing import List, Dict, Optional
import cv2
import numpy as np
import pandas as pd
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import preprocess_image, enhance_contrast, remove_noise
from bubble_detection import extract_bubbles, detect_bubbles_advanced, get_bubble_statistics
from scoring import OMRScorer, create_sample_answer_key

class OMRProcessor:
    """Main class for processing OMR sheets."""
    
    def __init__(self, answer_key_file: str, rows: int = 20, cols: int = 5):
        """
        Initialize OMR processor.
        
        Args:
            answer_key_file: Path to answer key file
            rows: Number of rows (questions)
            cols: Number of columns (subjects/options)
        """
        self.answer_key_file = answer_key_file
        self.rows = rows
        self.cols = cols
        self.scorer = OMRScorer(answer_key_file)
    
    def process_single_sheet(self, image_path: str, student_id: str = "Unknown") -> Dict:
        """
        Process a single OMR sheet.
        
        Args:
            image_path: Path to the OMR sheet image
            student_id: Student identifier
            
        Returns:
            Dictionary containing processing results
        """
        try:
            # Preprocess image
            print(f"Processing image: {image_path}")
            preprocessed_img = preprocess_image(image_path)
            
            # Enhance contrast
            enhanced_img = enhance_contrast(preprocessed_img)
            
            # Extract bubbles
            bubbles = extract_bubbles(enhanced_img, self.rows, self.cols)
            
            # Get bubble statistics
            bubble_stats = get_bubble_statistics(bubbles)
            
            # Score the sheet
            subject_scores, total_score = self.scorer.score_omr(bubbles)
            
            # Generate detailed report
            report = self.scorer.generate_detailed_report(bubbles, student_id)
            report['image_path'] = image_path
            report['bubble_statistics'] = bubble_stats
            
            return report
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return {
                'student_id': student_id,
                'image_path': image_path,
                'error': str(e),
                'subject_scores': {},
                'total_score': 0
            }
    
    def process_batch(self, image_directory: str, output_file: str = "omr_results.csv") -> pd.DataFrame:
        """
        Process multiple OMR sheets in batch.
        
        Args:
            image_directory: Directory containing OMR sheet images
            output_file: Path to save results
            
        Returns:
            DataFrame with all results
        """
        image_dir = Path(image_directory)
        image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpeg"))
        
        if not image_files:
            print(f"No image files found in {image_directory}")
            return pd.DataFrame()
        
        results = []
        
        for i, image_file in enumerate(image_files):
            print(f"Processing {i+1}/{len(image_files)}: {image_file.name}")
            student_id = image_file.stem  # Use filename as student ID
            result = self.process_single_sheet(str(image_file), student_id)
            results.append(result)
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Save results
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
        
        return df
    
    def validate_processing(self, image_path: str) -> Dict:
        """
        Validate OMR processing without scoring.
        
        Args:
            image_path: Path to the OMR sheet image
            
        Returns:
            Validation results
        """
        try:
            preprocessed_img = preprocess_image(image_path)
            enhanced_img = enhance_contrast(preprocessed_img)
            bubbles = extract_bubbles(enhanced_img, self.rows, self.cols)
            bubble_stats = get_bubble_statistics(bubbles)
            
            return {
                'valid': True,
                'bubble_statistics': bubble_stats,
                'image_shape': preprocessed_img.shape,
                'message': 'Processing completed successfully'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'message': 'Processing failed'
            }

def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='OMR Evaluation System')
    parser.add_argument('--image', type=str, help='Path to single OMR sheet image')
    parser.add_argument('--batch', type=str, help='Directory containing multiple OMR sheets')
    parser.add_argument('--answer-key', type=str, required=True, help='Path to answer key file')
    parser.add_argument('--rows', type=int, default=20, help='Number of rows (questions)')
    parser.add_argument('--cols', type=int, default=5, help='Number of columns (subjects)')
    parser.add_argument('--output', type=str, default='omr_results.csv', help='Output file for results')
    parser.add_argument('--create-sample-key', action='store_true', help='Create a sample answer key file')
    
    args = parser.parse_args()
    
    # Create sample answer key if requested
    if args.create_sample_key:
        sample_key_file = 'sample_answer_key.json'
        create_sample_answer_key(sample_key_file, args.rows, args.cols)
        print(f"Sample answer key created: {sample_key_file}")
        return
    
    # Initialize processor
    processor = OMRProcessor(args.answer_key, args.rows, args.cols)
    
    # Process single image
    if args.image:
        result = processor.process_single_sheet(args.image)
        print("\nProcessing Result:")
        print(f"Student ID: {result.get('student_id', 'Unknown')}")
        print(f"Total Score: {result.get('total_score', 0)}")
        print(f"Subject Scores: {result.get('subject_scores', {})}")
        
        if 'error' in result:
            print(f"Error: {result['error']}")
    
    # Process batch
    elif args.batch:
        df = processor.process_batch(args.batch, args.output)
        if not df.empty:
            print(f"\nBatch processing completed. Processed {len(df)} sheets.")
            print(f"Average score: {df['total_score'].mean():.2f}")
            print(f"Highest score: {df['total_score'].max()}")
            print(f"Lowest score: {df['total_score'].min()}")
    
    else:
        print("Please provide either --image or --batch argument")

if __name__ == "__main__":
    main()
