
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional
import numpy as np

class ImprovedOMRScorer:
    """Improved OMR scorer that handles multiple correct answers."""
    
    def __init__(self, answer_key_file: str):
        """
        Initialize scorer with answer key file.
        
        Args:
            answer_key_file: Path to the answer key file (JSON)
        """
        self.answer_key_file = answer_key_file
        self.answer_key = self._load_answer_key()
    
    def _load_answer_key(self) -> Dict:
        """Load answer key from file."""
        with open(self.answer_key_file, 'r') as f:
            return json.load(f)
    
    def score_omr_with_multiple_correct(self, detected_answers: List[List[int]], 
                                      subject_mapping: Optional[Dict[int, str]] = None) -> Tuple[Dict[str, int], int]:
        """
        Score OMR sheet allowing multiple correct answers per question.
        
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
                question_key = f"Q{row_idx+1}"
                
                if question_key in self.answer_key:
                    # Get correct answers for this question and subject
                    correct_answer = self.answer_key[question_key].get(f"Subject_{col_idx+1}", 0)
                    detected_answer = detected_answers[row_idx][col_idx] if col_idx < len(detected_answers[row_idx]) else 0
                    
                    # Award marks if student selected any correct option
                    if detected_answer == 1 and correct_answer == 1:
                        correct_answers += 1
                    # Also check if there are multiple correct answers in other subjects
                    elif detected_answer == 1:
                        # Check if any other subject has the correct answer for this question
                        has_correct_in_other_subject = False
                        for other_subject in self.answer_key[question_key]:
                            if self.answer_key[question_key][other_subject] == 1:
                                has_correct_in_other_subject = True
                                break
                        
                        # If there are correct answers in other subjects, award partial credit
                        if has_correct_in_other_subject:
                            correct_answers += 0.5  # Partial credit for selecting a correct option
            
            subject_scores[subject_name] = int(correct_answers)
            total_score += int(correct_answers)
        
        return subject_scores, total_score
    
    def score_omr_flexible(self, detected_answers: List[List[int]], 
                          subject_mapping: Optional[Dict[int, str]] = None) -> Tuple[Dict[str, float], float]:
        """
        Flexible scoring that awards full marks for any correct selection.
        
        Args:
            detected_answers: 2D list of detected bubble markings
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
        
        # Score each subject
        for col_idx, subject_name in subject_mapping.items():
            if col_idx >= len(detected_answers[0]):
                continue
                
            subject_score = 0.0
            total_questions = len(detected_answers)
            
            for row_idx in range(total_questions):
                question_key = f"Q{row_idx+1}"
                
                if question_key in self.answer_key:
                    detected_answer = detected_answers[row_idx][col_idx] if col_idx < len(detected_answers[row_idx]) else 0
                    
                    if detected_answer == 1:
                        # Check if this subject has the correct answer
                        correct_answer = self.answer_key[question_key].get(f"Subject_{col_idx+1}", 0)
                        
                        if correct_answer == 1:
                            subject_score += 1.0  # Full marks for correct answer
                        else:
                            # Check if there are any correct answers for this question
                            has_any_correct = any(self.answer_key[question_key].values())
                            if has_any_correct:
                                subject_score += 0.5  # Partial credit for selecting when there are correct answers
            
            subject_scores[subject_name] = subject_score
            total_score += subject_score
        
        return subject_scores, total_score
    
    def generate_detailed_report_flexible(self, detected_answers: List[List[int]], 
                                        student_id: str = "Unknown") -> Dict:
        """
        Generate detailed scoring report with flexible scoring.
        
        Args:
            detected_answers: 2D list of detected bubble markings
            student_id: Student identifier
            
        Returns:
            Detailed report dictionary
        """
        subject_scores, total_score = self.score_omr_flexible(detected_answers)
        
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
            'scoring_method': 'flexible_multiple_correct'
        }
        
        return report
