#!/usr/bin/env python3
"""
Process OMR Sets - Batch processing for Set 1 and Set 2
"""

import os
import sys
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import OMRProcessor
from excel_to_json_converter import convert_excel_to_json

class SetProcessor:
    """Process OMR sets with Excel answer keys."""
    
    def __init__(self):
        self.set1_processor = None
        self.set2_processor = None
        self.results = []
    
    def setup_set1(self, excel_answer_key, rows=20, cols=5):
        """Setup Set 1 processor with Excel answer key."""
        print("Setting up Set 1...")
        
        # Convert Excel to JSON if needed
        json_key_file = "answers/set1_answer_key.json"
        if excel_answer_key.endswith(('.xlsx', '.xls')):
            print(f"Converting Excel answer key: {excel_answer_key}")
            convert_excel_to_json(excel_answer_key, json_key_file)
        else:
            json_key_file = excel_answer_key
        
        # Initialize processor
        self.set1_processor = OMRProcessor(json_key_file, rows, cols)
        print(f"✓ Set 1 processor ready with {rows} rows and {cols} columns")
    
    def setup_set2(self, excel_answer_key, rows=20, cols=5):
        """Setup Set 2 processor with Excel answer key."""
        print("Setting up Set 2...")
        
        # Convert Excel to JSON if needed
        json_key_file = "answers/set2_answer_key.json"
        if excel_answer_key.endswith(('.xlsx', '.xls')):
            print(f"Converting Excel answer key: {excel_answer_key}")
            convert_excel_to_json(excel_answer_key, json_key_file)
        else:
            json_key_file = excel_answer_key
        
        # Initialize processor
        self.set2_processor = OMRProcessor(json_key_file, rows, cols)
        print(f"✓ Set 2 processor ready with {rows} rows and {cols} columns")
    
    def process_set1_papers(self):
        """Process all papers in Set 1."""
        if not self.set1_processor:
            print("❌ Set 1 processor not initialized")
            return
        
        print("\nProcessing Set 1 papers...")
        set1_dir = Path("set1_papers")
        
        if not set1_dir.exists():
            print(f"❌ Set 1 papers directory not found: {set1_dir}")
            return
        
        # Get all image files
        image_files = list(set1_dir.glob("*.jpg")) + list(set1_dir.glob("*.png")) + list(set1_dir.glob("*.jpeg"))
        
        if not image_files:
            print(f"❌ No image files found in {set1_dir}")
            return
        
        print(f"Found {len(image_files)} papers in Set 1")
        
        # Process each paper
        for i, image_file in enumerate(image_files):
            print(f"Processing {i+1}/{len(image_files)}: {image_file.name}")
            
            try:
                student_id = f"SET1_{image_file.stem}"
                result = self.set1_processor.process_single_sheet(str(image_file), student_id)
                result['set'] = 'Set 1'
                result['paper_file'] = image_file.name
                self.results.append(result)
                
                print(f"  ✓ Score: {result.get('total_score', 0)}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.results.append({
                    'student_id': f"SET1_{image_file.stem}",
                    'set': 'Set 1',
                    'paper_file': image_file.name,
                    'error': str(e),
                    'total_score': 0
                })
    
    def process_set2_papers(self):
        """Process all papers in Set 2."""
        if not self.set2_processor:
            print("❌ Set 2 processor not initialized")
            return
        
        print("\nProcessing Set 2 papers...")
        set2_dir = Path("set2_papers")
        
        if not set2_dir.exists():
            print(f"❌ Set 2 papers directory not found: {set2_dir}")
            return
        
        # Get all image files
        image_files = list(set2_dir.glob("*.jpg")) + list(set2_dir.glob("*.png")) + list(set2_dir.glob("*.jpeg"))
        
        if not image_files:
            print(f"❌ No image files found in {set2_dir}")
            return
        
        print(f"Found {len(image_files)} papers in Set 2")
        
        # Process each paper
        for i, image_file in enumerate(image_files):
            print(f"Processing {i+1}/{len(image_files)}: {image_file.name}")
            
            try:
                student_id = f"SET2_{image_file.stem}"
                result = self.set2_processor.process_single_sheet(str(image_file), student_id)
                result['set'] = 'Set 2'
                result['paper_file'] = image_file.name
                self.results.append(result)
                
                print(f"  ✓ Score: {result.get('total_score', 0)}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.results.append({
                    'student_id': f"SET2_{image_file.stem}",
                    'set': 'Set 2',
                    'paper_file': image_file.name,
                    'error': str(e),
                    'total_score': 0
                })
    
    def generate_report(self, output_file="omr_results_combined.csv"):
        """Generate combined report for both sets."""
        if not self.results:
            print("❌ No results to report")
            return
        
        print(f"\nGenerating report: {output_file}")
        
        # Convert to DataFrame
        df = pd.DataFrame(self.results)
        
        # Add timestamp
        df['processed_at'] = datetime.now().isoformat()
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        # Print summary
        print("\n" + "="*50)
        print("PROCESSING SUMMARY")
        print("="*50)
        
        total_papers = len(df)
        successful_papers = len(df[df['total_score'] > 0])
        
        print(f"Total papers processed: {total_papers}")
        print(f"Successful processing: {successful_papers}")
        print(f"Success rate: {successful_papers/total_papers*100:.1f}%")
        
        if 'set' in df.columns:
            set1_count = len(df[df['set'] == 'Set 1'])
            set2_count = len(df[df['set'] == 'Set 2'])
            print(f"Set 1 papers: {set1_count}")
            print(f"Set 2 papers: {set2_count}")
        
        if 'total_score' in df.columns:
            print(f"Average score: {df['total_score'].mean():.1f}")
            print(f"Highest score: {df['total_score'].max()}")
            print(f"Lowest score: {df['total_score'].min()}")
        
        print(f"\nResults saved to: {output_file}")
        
        return df
    
    def process_both_sets(self, set1_excel_key, set2_excel_key, rows=20, cols=5):
        """Process both sets with their respective answer keys."""
        print("OMR Set Processing - Set 1 & Set 2")
        print("="*50)
        
        # Setup both processors
        self.setup_set1(set1_excel_key, rows, cols)
        self.setup_set2(set2_excel_key, rows, cols)
        
        # Process both sets
        self.process_set1_papers()
        self.process_set2_papers()
        
        # Generate combined report
        return self.generate_report()

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process OMR Sets 1 and 2')
    parser.add_argument('--set1-key', type=str, help='Set 1 answer key (Excel or JSON)')
    parser.add_argument('--set2-key', type=str, help='Set 2 answer key (Excel or JSON)')
    parser.add_argument('--rows', type=int, default=20, help='Number of rows (questions)')
    parser.add_argument('--cols', type=int, default=5, help='Number of columns (subjects)')
    parser.add_argument('--output', type=str, default='omr_results_combined.csv', help='Output file')
    
    args = parser.parse_args()
    
    if not args.set1_key or not args.set2_key:
        print("Usage: python process_sets.py --set1-key <file> --set2-key <file>")
        print("Example: python process_sets.py --set1-key excel_answer_keys/set1.xlsx --set2-key excel_answer_keys/set2.xlsx")
        return
    
    # Initialize processor
    processor = SetProcessor()
    
    # Process both sets
    df = processor.process_both_sets(args.set1_key, args.set2_key, args.rows, args.cols)
    
    if df is not None:
        print("\n🎉 Processing completed successfully!")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()
