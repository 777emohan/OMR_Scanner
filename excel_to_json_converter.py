#!/usr/bin/env python3
"""
Excel to JSON Answer Key Converter
Converts Excel answer keys to JSON format for OMR processing
"""

import pandas as pd
import json
import sys
from pathlib import Path

def convert_excel_to_json(excel_file, output_file=None, sheet_name=None):
    """
    Convert Excel answer key to JSON format.
    
    Args:
        excel_file: Path to Excel file
        output_file: Output JSON file path (optional)
        sheet_name: Specific sheet name (optional)
        
    Returns:
        Dictionary containing the answer key
    """
    try:
        # Read Excel file
        if sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
        else:
            df = pd.read_excel(excel_file)
        
        print(f"Excel file loaded successfully: {excel_file}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Convert to JSON format
        answer_key = {}
        
        # Assume first column is question numbers, rest are subjects
        question_col = df.columns[0]
        subject_cols = df.columns[1:]
        
        for idx, row in df.iterrows():
            question_num = row[question_col]
            
            # Handle different question number formats
            if pd.isna(question_num):
                continue
                
            # Convert to string and ensure Q prefix
            if isinstance(question_num, (int, float)):
                question_key = f"Q{int(question_num)}"
            else:
                question_key = str(question_num)
                if not question_key.startswith('Q'):
                    question_key = f"Q{question_key}"
            
            # Create subject answers
            subject_answers = {}
            for i, subject_col in enumerate(subject_cols):
                subject_name = f"Subject_{i+1}"
                answer_value = row[subject_col]
                
                # Convert answer to 0 or 1
                if pd.isna(answer_value):
                    subject_answers[subject_name] = 0
                elif isinstance(answer_value, (int, float)):
                    subject_answers[subject_name] = 1 if answer_value == 1 else 0
                elif isinstance(answer_value, str):
                    # Handle text answers like "A", "B", "C", "D", "E" or "1", "2", "3", "4", "5"
                    answer_value = answer_value.upper().strip()
                    if answer_value in ['A', '1']:
                        subject_answers[subject_name] = 1
                    elif answer_value in ['B', '2']:
                        subject_answers[f"Subject_{i+2}"] = 1 if i+2 <= len(subject_cols) else 0
                        subject_answers[subject_name] = 0
                    elif answer_value in ['C', '3']:
                        subject_answers[f"Subject_{i+3}"] = 1 if i+3 <= len(subject_cols) else 0
                        subject_answers[subject_name] = 0
                    elif answer_value in ['D', '4']:
                        subject_answers[f"Subject_{i+4}"] = 1 if i+4 <= len(subject_cols) else 0
                        subject_answers[subject_name] = 0
                    elif answer_value in ['E', '5']:
                        subject_answers[f"Subject_{i+5}"] = 1 if i+5 <= len(subject_cols) else 0
                        subject_answers[subject_name] = 0
                    else:
                        subject_answers[subject_name] = 0
                else:
                    subject_answers[subject_name] = 0
            
            answer_key[question_key] = subject_answers
        
        # Save to JSON file
        if output_file is None:
            output_file = excel_file.replace('.xlsx', '.json').replace('.xls', '.json')
        
        with open(output_file, 'w') as f:
            json.dump(answer_key, f, indent=2)
        
        print(f"Answer key converted and saved to: {output_file}")
        print(f"Total questions: {len(answer_key)}")
        print(f"Subjects per question: {len(subject_answers)}")
        
        return answer_key
        
    except Exception as e:
        print(f"Error converting Excel file: {e}")
        return None

def preview_excel_structure(excel_file, sheet_name=None):
    """
    Preview the structure of an Excel file.
    
    Args:
        excel_file: Path to Excel file
        sheet_name: Specific sheet name (optional)
    """
    try:
        if sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
        else:
            df = pd.read_excel(excel_file)
        
        print(f"\nExcel File Structure: {excel_file}")
        print("=" * 50)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
        
        return df
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python excel_to_json_converter.py <excel_file> [output_file] [sheet_name]")
        print("Example: python excel_to_json_converter.py answer_key.xlsx set1_answer_key.json")
        return
    
    excel_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Preview structure first
    print("Previewing Excel structure...")
    preview_excel_structure(excel_file, sheet_name)
    
    # Convert to JSON
    print("\nConverting to JSON...")
    answer_key = convert_excel_to_json(excel_file, output_file, sheet_name)
    
    if answer_key:
        print("\nConversion completed successfully!")
    else:
        print("\nConversion failed!")

if __name__ == "__main__":
    main()
