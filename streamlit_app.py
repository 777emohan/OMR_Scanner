import streamlit as st
import os
import sys
import tempfile
import pandas as pd
from pathlib import Path
import json
import cv2
import numpy as np
from PIL import Image

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing import preprocess_image, enhance_contrast
from bubble_detection import extract_bubbles, get_bubble_statistics
from scoring import OMRScorer, create_sample_answer_key

# Page configuration
st.set_page_config(
    page_title="OMR Evaluation System",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">📝 OMR Evaluation System</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Answer key selection
        answer_key_file = st.selectbox(
            "Select Answer Key",
            options=["answers/answer_key_v1.json", "answers/answer_key_v2.json"],
            help="Choose the answer key for the exam version"
        )
        
        # Grid configuration
        st.subheader("Grid Configuration")
        rows = st.number_input("Number of Rows (Questions)", min_value=1, max_value=100, value=20)
        cols = st.number_input("Number of Columns (Subjects)", min_value=1, max_value=20, value=5)
        
        # Processing options
        st.subheader("Processing Options")
        show_debug = st.checkbox("Show Debug Information", value=False)
        auto_detect_grid = st.checkbox("Auto-detect Grid Size", value=False)
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Single Sheet", "📁 Batch Processing", "📊 Results", "🔧 Tools"])
    
    with tab1:
        single_sheet_processing(answer_key_file, rows, cols, show_debug, auto_detect_grid)
    
    with tab2:
        batch_processing(answer_key_file, rows, cols, show_debug)
    
    with tab3:
        results_viewer()
    
    with tab4:
        tools_section()

def single_sheet_processing(answer_key_file, rows, cols, show_debug, auto_detect_grid):
    """Single sheet processing interface."""
    st.header("Single Sheet Processing")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload OMR Sheet Image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the OMR sheet"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Original Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded OMR Sheet", use_column_width=True)
        
        with col2:
            st.subheader("Processing Options")
            student_id = st.text_input("Student ID", value=uploaded_file.name.split('.')[0])
            process_button = st.button("Process Sheet", type="primary")
        
        if process_button:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    image.save(tmp_file.name)
                    tmp_path = tmp_file.name
                
                # Process the image
                with st.spinner("Processing OMR sheet..."):
                    # Preprocess image
                    preprocessed_img = preprocess_image(tmp_path)
                    enhanced_img = enhance_contrast(preprocessed_img)
                    
                    # Extract bubbles
                    if auto_detect_grid:
                        # Auto-detect grid size (simplified)
                        bubbles = extract_bubbles(enhanced_img, rows, cols)
                    else:
                        bubbles = extract_bubbles(enhanced_img, rows, cols)
                    
                    # Load answer key and score
                    if os.path.exists(answer_key_file):
                        scorer = OMRScorer(answer_key_file)
                        subject_scores, total_score = scorer.score_omr(bubbles)
                        report = scorer.generate_detailed_report(bubbles, student_id)
                    else:
                        st.error(f"Answer key file not found: {answer_key_file}")
                        return
                
                # Display results
                st.success("Processing completed successfully!")
                
                # Results metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Score", total_score)
                with col2:
                    st.metric("Percentage", f"{report.get('percentage', 0):.1f}%")
                with col3:
                    st.metric("Questions", report.get('total_questions', 0))
                with col4:
                    st.metric("Multiple Selections", report.get('multiple_selections', 0))
                
                # Subject-wise scores
                st.subheader("Subject-wise Scores")
                subject_df = pd.DataFrame(list(subject_scores.items()), columns=['Subject', 'Score'])
                st.dataframe(subject_df, use_container_width=True)
                
                # Debug information
                if show_debug:
                    st.subheader("Debug Information")
                    bubble_stats = get_bubble_statistics(bubbles)
                    st.json(bubble_stats)
                    
                    # Show processed image
                    st.subheader("Processed Image")
                    st.image(enhanced_img, caption="Enhanced Image", use_column_width=True)
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"Error processing sheet: {str(e)}")
                if show_debug:
                    st.exception(e)

def batch_processing(answer_key_file, rows, cols, show_debug):
    """Batch processing interface."""
    st.header("Batch Processing")
    
    # File upload for multiple files
    uploaded_files = st.file_uploader(
        "Upload Multiple OMR Sheet Images",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        help="Upload multiple OMR sheet images for batch processing"
    )
    
    if uploaded_files:
        st.info(f"Uploaded {len(uploaded_files)} files")
        
        if st.button("Process All Sheets", type="primary"):
            results = []
            
            # Process each file
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    status_text.text(f"Processing {uploaded_file.name}...")
                    
                    # Save file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        image = Image.open(uploaded_file)
                        image.save(tmp_file.name)
                        tmp_path = tmp_file.name
                    
                    # Process image
                    preprocessed_img = preprocess_image(tmp_path)
                    enhanced_img = enhance_contrast(preprocessed_img)
                    bubbles = extract_bubbles(enhanced_img, rows, cols)
                    
                    # Score
                    if os.path.exists(answer_key_file):
                        scorer = OMRScorer(answer_key_file)
                        subject_scores, total_score = scorer.score_omr(bubbles)
                        report = scorer.generate_detailed_report(bubbles, uploaded_file.name.split('.')[0])
                        results.append(report)
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    results.append({
                        'student_id': uploaded_file.name.split('.')[0],
                        'error': str(e),
                        'total_score': 0
                    })
            
            # Display results
            if results:
                st.success(f"Processed {len(results)} sheets successfully!")
                
                # Convert to DataFrame
                df = pd.DataFrame(results)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sheets", len(df))
                with col2:
                    st.metric("Average Score", f"{df['total_score'].mean():.1f}")
                with col3:
                    st.metric("Success Rate", f"{len(df[df['total_score'] > 0]) / len(df) * 100:.1f}%")
                
                # Results table
                st.subheader("Results Table")
                st.dataframe(df, use_container_width=True)
                
                # Download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="omr_results.csv",
                    mime="text/csv"
                )

def results_viewer():
    """Results viewer interface."""
    st.header("Results Viewer")
    
    # Upload results file
    results_file = st.file_uploader(
        "Upload Results CSV File",
        type=['csv'],
        help="Upload a previously generated results CSV file"
    )
    
    if results_file is not None:
        try:
            df = pd.read_csv(results_file)
            st.success("Results loaded successfully!")
            
            # Display summary
            st.subheader("Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Students", len(df))
            with col2:
                st.metric("Average Score", f"{df['total_score'].mean():.1f}")
            with col3:
                st.metric("Highest Score", df['total_score'].max())
            with col4:
                st.metric("Lowest Score", df['total_score'].min())
            
            # Display results table
            st.subheader("Detailed Results")
            st.dataframe(df, use_container_width=True)
            
            # Charts
            if 'total_score' in df.columns:
                st.subheader("Score Distribution")
                st.bar_chart(df['total_score'].value_counts().sort_index())
            
        except Exception as e:
            st.error(f"Error loading results: {str(e)}")

def tools_section():
    """Tools and utilities section."""
    st.header("Tools & Utilities")
    
    # Create sample answer key
    st.subheader("Create Sample Answer Key")
    col1, col2 = st.columns(2)
    
    with col1:
        sample_rows = st.number_input("Number of Questions", min_value=1, max_value=100, value=20)
    with col2:
        sample_cols = st.number_input("Number of Subjects", min_value=1, max_value=20, value=5)
    
    if st.button("Generate Sample Answer Key"):
        try:
            sample_key_file = "sample_answer_key.json"
            create_sample_answer_key(sample_key_file, sample_rows, sample_cols)
            st.success(f"Sample answer key created: {sample_key_file}")
            
            # Display the generated key
            with open(sample_key_file, 'r') as f:
                key_data = json.load(f)
            st.json(key_data)
            
        except Exception as e:
            st.error(f"Error creating sample key: {str(e)}")
    
    # System information
    st.subheader("System Information")
    st.info("OMR Evaluation System v1.0")
    st.info("Built with OpenCV, Streamlit, and Python")

if __name__ == "__main__":
    main()
