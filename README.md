# 🎓 EduPredict - Academic Success Predictor

**EduPredict** is an AI-powered academic performance prediction dashboard that helps identify students at risk of dropout or underperformance using tuned machine learning models and rich, interactive visualizations.

---

## 📁 Project Structure

```
EduPredict_Project/
│
├── app/
│   └── edu_predict_app.py
├── data/
│   ├── academic_raw.csv
│   └── academic_cleaned.csv
├── models/
│   ├── rf_model.pkl                         # Baseline classifier (fallback)
│   ├── tuned_logistic_regression_model.pkl  # Tuned classifier
│   ├── tuned_random_forest_model.pkl        # Tuned classifier (often best)
│   ├── tuned_xgboost_model.pkl              # Tuned classifier
│   ├── anomaly_model.pkl                    # Isolation Forest (outlier detection)
│   └── trend_model.pkl                      # Trend model (Sem-2 prediction)
├── notebooks/
│   ├── EDA.ipynb
│   └── Modeling.ipynb
├── reports/
│   ├── EDA_Report.html
│   ├── model_comparison.csv
│   └── model_comparison_tuned.csv           # Used to auto-pick best tuned model
├── assets/
│   ├── flowchart.svg
│   ├── dfd_level0.svg
│   └── screenshots/
│       ├── 01_Login_Form.png
│       ├── 02_Prediction_Form.png
│       ├── 03_Prediction_Output.png
│       ├── 04_Downloaded_Report.png
│       ├── 05_Advance_Charts.png
│       └── 06_Recommendation_Hub.png
├── requirements.txt
└── README.md
```

---

## 🚀 Key Features

- 🔐 Role-based Login (Student / Teacher / Counselor)
- 🔮 Predict Academic Status: Dropout / Enrolled / Graduate
- 🤖 Tuned models auto-selected by best F1 (from `reports/model_comparison_tuned.csv`)
- ⚙️ Optional Advanced model selector (hidden unless multiple models exist)
- 🚨 Anomaly Detection (Isolation Forest)
- 📈 Semester Grade Forecasting (Trend Prediction)
- 📊 Interactive Visualizations and Advanced Analytics
  - Correlation heatmap (numeric features)
  - 3D performance scatter (Admission vs Sem-1 vs Sem-2)
  - Dropout heatmap by Age Group × Scholarship
  - Normalized stacked bar of Grade distribution by Course
  - Violin plot of Admission grade by Outcome
  - Parallel categories: Gender → Scholarship → Outcome
- 📄 Report Download as TXT
- 📬 Google Form Feedback Integration
- ✨ Modern UI Styling (Streamlit + CSS + Animations)

---

## 🧠 Machine Learning Models Used

| Purpose                | Model Used (Deployed)                           |
|------------------------|--------------------------------------------------|
| Academic Status        | Tuned RF / Tuned LR / Tuned XGBoost (auto-best) |
| Anomaly Detection      | Isolation Forest                                 |
| Grade Trend Prediction | Linear Regression                                |

---

## 📊 Dataset Details

- 📌 **Source:** UCI ML Repository (#697)
- 👥 **Records:** ~4500 Students
- 🧾 **Features:** Age, Grades, Gender, Economic Indicators, Course Info
- 🎯 **Target:** Dropout / Enrolled / Graduate

---

## 🛠️ Tech Stack

| Area     | Tools / Libraries                |
|----------|----------------------------------|
| Language | Python 3.11                      |
| ML       | scikit-learn, XGBoost, joblib    |
| Dashboard| Streamlit, Plotly, Lottie        |
| Styling  | HTML, CSS, Google Fonts          |
| Hosting  | Local / Streamlit Cloud (Optional)|

---

## 📦 How to Run Locally

### Option 1: Standard Run (with warning suppression)
```bash
streamlit run app/edu_predict_app.py
```

### Option 2: Clean Run (no warnings)
```bash
python run_app_clean.py
```

### Option 3: Retrain Models (if you encounter version warnings)
```bash
python retrain_models.py
```

> Make sure you have Python 3.10+ and pip installed.

1. **Clone this repository or unzip it:**
   ```bash
   git clone https://github.com/ShehzilxCode/Edu-Predict-Sem6.git
   cd Edu-Predict-Sem6

   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   If you plan to export charts as PNG from the app, also install:
   ```bash
   pip install kaleido
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app/edu_predict_app.py
   ```

4. **Login with:**
   - **Student:** `student` / `studentpass`
   - **Teacher:** `teacher` / `teacherpass`
   - **Counselor:** `counselor` / `counselpass`

---

## 📸 Dashboard Preview (Screenshots)

See `assets/screenshots` for screenshots

---

## 📥 Feedback Integration

Google Form is integrated for collecting feedback: 
🔗 **[Submit Feedback Here](https://forms.gle/dEW6AfgRSia92J438)**

---

## ✅ Final Deliverables

- ✅ Cleaned Dataset
- ✅ Trained Models (.pkl)
- ✅ Tuned Model Comparison (`reports/model_comparison_tuned.csv`)
- ✅ Full Dashboard Code
- ✅ Flowchart & DFD Diagrams
- ✅ Feedback Integration
- ✅ Video Demonstration (optional)
- ✅ Documentation (README, Report)

---

## 📚 License

This project is built for academic & educational purposes only. All rights to the dataset belong to the UCI ML Repository.

---

## 🙌 Acknowledgments

- UCI Machine Learning Repository
- Streamlit Team
- Scikit-learn, XGBoost, Plotly
- Teachers & Evaluators guiding this project