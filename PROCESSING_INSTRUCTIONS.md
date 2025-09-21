
# OMR Set Processing Instructions

## Step 1: Prepare Answer Keys
1. Place your Excel answer key files in the `excel_answer_keys/` folder
2. Name them as `set1_answer_key.xlsx` and `set2_answer_key.xlsx`
3. Follow the format in `sample_answer_key_template.xlsx`

## Step 2: Prepare Answer Sheets
1. Take photos of Set 1 answer sheets
2. Place them in the `set1_papers/` folder
3. Take photos of Set 2 answer sheets  
4. Place them in the `set2_papers/` folder

## Step 3: Process the Sets
Run one of these commands:

### Option 1: Process both sets together
```bash
python process_sets.py --set1-key excel_answer_keys/set1_answer_key.xlsx --set2-key excel_answer_keys/set2_answer_key.xlsx
```

### Option 2: Process sets individually
```bash
# Set 1 only
python src/main.py --batch set1_papers/ --answer-key answers/set1_answer_key.json --output results/set1_results.csv

# Set 2 only  
python src/main.py --batch set2_papers/ --answer-key answers/set2_answer_key.json --output results/set2_results.csv
```

### Option 3: Use web interface
```bash
streamlit run streamlit_app.py
```

## Step 4: View Results
- Results will be saved in the `results/` folder
- Open the CSV files to view detailed scores
- Use the web interface for visual analysis

## Tips for Best Results
1. Take clear, well-lit photos
2. Keep the camera straight (avoid angles)
3. Ensure the entire answer sheet is visible
4. Use consistent naming for answer sheets
5. Test with a few sheets first before batch processing
