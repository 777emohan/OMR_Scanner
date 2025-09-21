# Your OMR Processing Workflow

## 📁 Folder Structure Created

```
omr_evaluator/
├── set1_papers/          # 📸 Place Set 1 answer sheet photos here
├── set2_papers/          # 📸 Place Set 2 answer sheet photos here
├── excel_answer_keys/    # 📊 Place your Excel answer keys here
├── results/              # 📋 Processed results will be saved here
└── [other system files]
```

## 🚀 Quick Start (3 Steps)

### Step 1: Prepare Your Files
1. **Excel Answer Keys**: Place your answer key Excel files in `excel_answer_keys/` folder
   - Name them as `set1_answer_key.xlsx` and `set2_answer_key.xlsx`
   - Follow the format in `sample_answer_key_template.xlsx`

2. **Set 1 Photos**: Place Set 1 answer sheet photos in `set1_papers/` folder
   - Supported formats: `.jpg`, `.png`, `.jpeg`
   - Take clear, well-lit photos

3. **Set 2 Photos**: Place Set 2 answer sheet photos in `set2_papers/` folder
   - Same requirements as Set 1

### Step 2: Process Everything
Run this simple command:
```bash
python quick_process.py
```

### Step 3: Get Results
- Results will be saved in `results/` folder
- Open the CSV files to view detailed scores
- Use the web interface for visual analysis: `streamlit run streamlit_app.py`

## 📊 Excel Answer Key Format

Your Excel files should look like this:

| Question | Subject_1 | Subject_2 | Subject_3 | Subject_4 | Subject_5 |
|----------|-----------|-----------|-----------|-----------|-----------|
| Q1       | 1         | 0         | 0         | 0         | 0         |
| Q2       | 0         | 1         | 0         | 0         | 0         |
| Q3       | 0         | 0         | 1         | 0         | 0         |
| ...      | ...       | ...       | ...       | ...       | ...       |

- **Question**: Question number (Q1, Q2, Q3, ...)
- **Subject_1 to Subject_5**: 1 for correct answer, 0 for incorrect

## 🎯 Alternative Processing Methods

### Method 1: Process Both Sets Together
```bash
python process_sets.py --set1-key excel_answer_keys/set1_answer_key.xlsx --set2-key excel_answer_keys/set2_answer_key.xlsx
```

### Method 2: Process Sets Individually
```bash
# Set 1 only
python src/main.py --batch set1_papers/ --answer-key answers/set1_answer_key.json --output results/set1_results.csv

# Set 2 only
python src/main.py --batch set2_papers/ --answer-key answers/set2_answer_key.json --output results/set2_results.csv
```

### Method 3: Web Interface
```bash
streamlit run streamlit_app.py
```
Then open your browser to `http://localhost:8501`

## 📸 Photo Tips for Best Results

1. **Lighting**: Take photos in good, even lighting
2. **Angle**: Keep camera straight (avoid angles)
3. **Distance**: Ensure entire answer sheet is visible
4. **Focus**: Make sure text and bubbles are clear
5. **Background**: Use a clean, contrasting background

## 🔧 Troubleshooting

### Common Issues:
1. **"No files found"**: Check folder names and file locations
2. **"Excel conversion failed"**: Verify Excel format matches template
3. **"Processing failed"**: Check photo quality and try again
4. **"Low accuracy"**: Ensure photos are clear and well-lit

### Getting Help:
- Check `PROCESSING_INSTRUCTIONS.md` for detailed instructions
- Run `python test_omr.py` to test the system
- Use the web interface for visual debugging

## 📋 Expected Output

After processing, you'll get:
- **Combined Results**: `omr_results_combined.csv` with all scores
- **Individual Results**: Separate files for each set
- **Statistics**: Average scores, success rates, etc.
- **Detailed Reports**: Subject-wise scores and analysis

## 🎉 You're Ready!

1. Place your Excel answer keys in `excel_answer_keys/`
2. Place Set 1 photos in `set1_papers/`
3. Place Set 2 photos in `set2_papers/`
4. Run `python quick_process.py`
5. Check results in `results/` folder

**That's it! The system will handle everything else automatically.**
