import json
import csv
import pandas as pd
from typing import Dict, List, Tuple, Optional
import numpy as np

class OMRScorer:
    """Class to handle OMR scoring operations."""
    
    def __init__(self, answer_key_file: str):
        """
        Initialize scorer with answer key file.
        
        Args:
            answer_key_file: Path to the answer key file (JSON or CSV)
        """
        self.answer_key_file = answer_key_file
        self.answer_key = self._load_answer_key()
    
    def _load_answer_key(self) -> Dict:
        """Load answer key from file."""
        if self.answer_key_file.endswith('.json'):
            with open(self.answer_key_file, 'r') as f:
                return json.load(f)
        elif self.answer_key_file.endswith('.csv'):
            df = pd.read_csv(self.answer_key_file)
            return df.to_dict('index')
        else:
            raise ValueError("Unsupported file format. Use JSON or CSV.")
    
    def score_omr(self, detected_answers: List[List[int]], 
                  subject_mapping: Optional[Dict[int, str]] = None) -> Tuple[Dict[str, int], int]:
        """
        Score OMR sheet based on detected answers.
        
        Args:
            detected_answers: 2D list of detected bubble markings
            subject_mapping: Optional mapping of column indices to subject names
            
        Returns:
            Tuple of (subject_scores, total_score)
        """
        if not detected_answers:
            return {}, 0
        
        subject_scores = {}
        total_score = 0
        
        # If no subject mapping provided, create default one
        if subject_mapping is None:
            subject_mapping = {i: f"Subject_{i+1}" for i in range(len(detected_answers[0]))}
        
        # Score each subject
        for col_idx, subject_name in subject_mapping.items():
            if col_idx >= len(detected_answers[0]):
                continue
                
            correct_answers = 0
            total_questions = len(detected_answers)
            
            for row_idx in range(total_questions):
                if (row_idx < len(self.answer_key) and 
                    col_idx < len(detected_answers[row_idx]) and
                    detected_answers[row_idx][col_idx] == self.answer_key.get(f"Q{row_idx+1}", {}).get(f"Subject_{col_idx+1}", 0)):
                    correct_answers += 1
            
            subject_scores[subject_name] = correct_answers
            total_score += correct_answers
        
        return subject_scores, total_score
    
    def score_with_penalty(self, detected_answers: List[List[int]], 
                          correct_mark: int = 1, wrong_mark: int = -0.25,
                          subject_mapping: Optional[Dict[int, str]] = None) -> Tuple[Dict[str, float], float]:
        """
        Score OMR with penalty for wrong answers.
        
        Args:
            detected_answers: 2D list of detected bubble markings
            correct_mark: Points for correct answer
            wrong_mark: Points for wrong answer (negative)
            subject_mapping: Optional mapping of column indices to subject names
            
        Returns:
            Tuple of (subject_scores, total_score)
        """
        if not detected_answers:
            return {}, 0.0
        
        subject_scores = {}
        total_score = 0.0
        
        if subject_mapping is None:
            subject_mapping = {i: f"Subject_{i+1}" for i in range(len(detected_answers[0]))}
        
        for col_idx, subject_name in subject_mapping.items():
            if col_idx >= len(detected_answers[0]):
                continue
                
            subject_score = 0.0
            total_questions = len(detected_answers)
            
            for row_idx in range(total_questions):
                if row_idx < len(self.answer_key):
                    correct_answer = self.answer_key.get(f"Q{row_idx+1}", {}).get(f"Subject_{col_idx+1}", 0)
                    detected_answer = detected_answers[row_idx][col_idx] if col_idx < len(detected_answers[row_idx]) else 0
                    
                    if detected_answer == correct_answer:
                        subject_score += correct_mark
                    else:
                        subject_score += wrong_mark
            
            subject_scores[subject_name] = subject_score
            total_score += subject_score
        
        return subject_scores, total_score
    
    def generate_detailed_report(self, detected_answers: List[List[int]], 
                               student_id: str = "Unknown") -> Dict:
        """
        Generate detailed scoring report.
        
        Args:
            detected_answers: 2D list of detected bubble markings
            student_id: Student identifier
            
        Returns:
            Detailed report dictionary
        """
        subject_scores, total_score = self.score_omr(detected_answers)
        
        # Calculate statistics
        total_questions = len(detected_answers)
        total_subjects = len(detected_answers[0]) if detected_answers else 0
        max_possible_score = total_questions * total_subjects
        
        # Count multiple selections
        multiple_selections = sum(1 for row in detected_answers if sum(row) > 1)
        
        # Count unanswered questions
        unanswered = sum(1 for row in detected_answers if sum(row) == 0)
        
        report = {
            'student_id': student_id,
            'subject_scores': subject_scores,
            'total_score': total_score,
            'max_possible_score': max_possible_score,
            'percentage': (total_score / max_possible_score * 100) if max_possible_score > 0 else 0,
            'total_questions': total_questions,
            'total_subjects': total_subjects,
            'multiple_selections': multiple_selections,
            'unanswered_questions': unanswered,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return report

def create_sample_answer_key(output_file: str, rows: int = 20, cols: int = 5):
    """
    Create a sample answer key file for testing.
    
    Args:
        output_file: Path to save the answer key
        rows: Number of questions
        cols: Number of subjects/options
    """
    answer_key = {}
    
    for i in range(rows):
        question_key = f"Q{i+1}"
        answer_key[question_key] = {}
        
        for j in range(cols):
            subject_key = f"Subject_{j+1}"
            # Randomly assign correct answers (1) or incorrect (0)
            answer_key[question_key][subject_key] = np.random.randint(0, 2)
    
    with open(output_file, 'w') as f:
        json.dump(answer_key, f, indent=2)

def batch_score_omr_sheets(sheets_data: List[Dict], answer_key_file: str) -> pd.DataFrame:
    """
    Score multiple OMR sheets in batch.
    
    Args:
        sheets_data: List of dictionaries containing sheet data
        answer_key_file: Path to answer key file
        
    Returns:
        DataFrame with scoring results
    """
    scorer = OMRScorer(answer_key_file)
    results = []
    
    for sheet_data in sheets_data:
        student_id = sheet_data.get('student_id', 'Unknown')
        detected_answers = sheet_data.get('answers', [])
        
        report = scorer.generate_detailed_report(detected_answers, student_id)
        results.append(report)
    
    return pd.DataFrame(results)
