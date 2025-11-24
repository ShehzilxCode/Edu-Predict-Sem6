import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from datetime import datetime
import time
import warnings

# Suppress version compatibility warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.base")
warnings.filterwarnings("ignore", category=UserWarning, module="pickle")
warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")
warnings.filterwarnings("ignore", message=".*If you are loading a serialized model.*", category=UserWarning)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EduPredict | Future Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎓"
)

# --- UI THEME: FUTURISTIC GLASS & NEON ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;600&display=swap');

    /* --- GLOBAL VARIABLES --- */
    :root {
        --bg-dark: #0a0b1e;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --neon-blue: #00f2ff;
        --neon-purple: #bc13fe;
        --neon-green: #0aff60;
        --text-main: #ffffff;
        --text-muted: #a0a0b0;
    }

    /* --- ANIMATED BACKGROUND --- */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(188, 19, 254, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(0, 242, 255, 0.15) 0%, transparent 40%);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    h1, h2, h3, h4 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-main);
    }

    /* --- NEW HEADER STYLING --- */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        position: relative;
    }

    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(to bottom, #ffffff, #a5f3fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0, 242, 255, 0.4);
        line-height: 1.1;
    }

    .hero-subtitle {
        font-family: 'Rajdhani';
        color: var(--neon-blue);
        font-size: 1.2rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-top: 0.5rem;
        opacity: 0.8;
    }

    /* --- SYSTEM NOTICE BAR --- */
    .system-notice-bar {
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, rgba(255, 165, 0, 0.05) 0%, rgba(255, 165, 0, 0.1) 50%, rgba(255, 165, 0, 0.05) 100%);
        border-top: 1px solid rgba(255, 165, 0, 0.3);
        border-bottom: 1px solid rgba(255, 165, 0, 0.3);
        padding: 12px;
        margin-bottom: 30px;
        justify-content: center;
        gap: 15px;
    }

    .notice-icon {
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* --- GLASS CARDS --- */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* --- TAB 3 SPECIFIC STYLES --- */
    .rec-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid var(--neon-blue);
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0 12px 12px 0;
    }

    .rec-header {
        font-family: 'Rajdhani';
        font-size: 1.3rem;
        color: var(--neon-blue);
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    .story-card {
        background: rgba(10, 255, 96, 0.05);
        border: 1px solid rgba(10, 255, 96, 0.2);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* --- INPUT FIELDS --- */
    .stTextInput > div > div, 
    .stSelectbox > div > div, 
    .stNumberInput > div > div {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px;
        color: white !important;
    }

    .stSelectbox > div > div > div {
        color: white !important;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: transparent;
        color: var(--neon-blue);
        border: 1px solid var(--neon-blue);
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
        width: 100%;
    }

    .stButton > button:hover {
        background: var(--neon-blue);
        color: #000;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
        transform: scale(1.02);
    }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background-color: #050510;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.02);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-muted);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0, 242, 255, 0.1), rgba(188, 19, 254, 0.1));
        color: #fff !important;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }

    /* --- SLIDERS --- */
    .stSlider > div > div > div > div {
        background-color: var(--neon-blue);
    }

    /* --- RESULT CARDS --- */
    .result-card-glass {
        background: rgba(20, 20, 30, 0.6);
        border-left: 4px solid;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* --- FOOTER --- */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #050510;
        color: #a0a0b0;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        z-index: 999;
    }
    .footer a {
        color: var(--neon-blue);
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL VERSION ---
APP_VERSION = "1.0.0"  # Updated version number

# --- HEADER (REDESIGNED) ---
st.markdown("""
<div class='hero-container'>
    <h1 class='hero-title'>EDUPREDICT</h1>
    <div class='hero-subtitle'>AI-DRIVEN ACADEMIC INTELLIGENCE ARCHITECTURE</div>
</div>
""", unsafe_allow_html=True)

# --- SYSTEM NOTICE (REDESIGNED) ---
st.markdown(f"""
<div class='system-notice-bar'>
    <span class='notice-icon'>⚡</span>
    <span style='color: #ffd700; font-family: "Rajdhani"; letter-spacing: 1px; font-weight: 600;'>
        SYSTEM PROTOCOL v{APP_VERSION}: PREDICTIONS ARE SIMULATIONS. CONSULT HUMAN MENTORS FOR AUTHORIZED SUPPORT.
    </span>
</div>
""", unsafe_allow_html=True)

auth_users = {
    "student": "studentpass",
    "teacher": "teacherpass",
    "counselor": "counselpass"
}

# --- SIDEBAR ---
st.sidebar.markdown("""
<div style='text-align: center; padding: 1.5rem; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
    <h2 style='margin:0; font-family: "Rajdhani"; letter-spacing: 2px;'>ACCESS PORTAL</h2>
</div>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.sidebar:
        st.markdown(
            "<div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);'>",
            unsafe_allow_html=True)
        username = st.text_input("ID CODE", key="user", placeholder="e.g. student")
        password = st.text_input("ACCESS KEY", type="password", key="pass", placeholder="••••••")

        if st.button("INITIALIZE SESSION", use_container_width=True):
            if username in auth_users and password == auth_users[username]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("ACCESS GRANTED")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("ACCESS DENIED")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.sidebar.expander("🔑 DEMO CREDENTIALS"):
        st.code("Student: student / studentpass\nTeacher: teacher / teacherpass\nCounselor: counselor / counselpass")

if st.session_state.logged_in:
    role = st.session_state.username

    role_colors = {
        "student": "#00f2ff",  # Neon Blue
        "teacher": "#0aff60",  # Neon Green
        "counselor": "#bc13fe"  # Neon Purple
    }

    current_color = role_colors.get(role, "#ffffff")

    st.sidebar.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0.2) 100%); 
         padding: 1.5rem; border-radius: 16px; text-align: center; border: 1px solid {current_color}40; margin-bottom: 1rem;'>
        <div style='width: 60px; height: 60px; border-radius: 50%; background: {current_color}20; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; border: 1px solid {current_color}; box-shadow: 0 0 15px {current_color}40;'>
            {'👨‍🎓' if role == 'student' else '👩‍🏫' if role == 'teacher' else '🧠'}
        </div>
        <h3 style='color: {current_color}; margin: 0; letter-spacing: 1px;'>{role.upper()}</h3>
        <p style='color: #888; font-size: 0.8rem; margin-top: 5px;'>ONLINE • {datetime.now().strftime('%H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("TERMINATE SESSION", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Load Models & Data
    try:
        # Check if the data file exists at the expected path
        data_path = os.path.join(os.getcwd(), "data", "academic_cleaned.csv")
        if not os.path.exists(data_path):
            # Try a fallback if run from a different context
            data_path = "data/academic_cleaned.csv"
        df = pd.read_csv(data_path)


        # Load models
        def load_model_or_none(path):
            if os.path.exists(path):
                return joblib.load(path)
            return None


        models_dir = "models"
        anomaly_model = load_model_or_none(os.path.join(models_dir, "anomaly_model.pkl"))
        trend_model = load_model_or_none(os.path.join(models_dir, "trend_model.pkl"))

        candidate_files = [
            ("Tuned Logistic Regression", os.path.join(models_dir, "tuned_logistic_regression_model.pkl")),
            ("Tuned Random Forest", os.path.join(models_dir, "tuned_random_forest_model.pkl")),
            ("Tuned XGBoost", os.path.join(models_dir, "tuned_xgboost_model.pkl")),
            ("Baseline Random Forest", os.path.join(models_dir, "rf_model.pkl")),
        ]

        available_models = {}
        for display_name, path in candidate_files:
            model = load_model_or_none(path)
            if model:
                available_models[display_name] = model

        # Default Model Selection Logic
        default_model_name = list(available_models.keys())[0] if available_models else None

        models_loaded = len(available_models) > 0 and anomaly_model is not None and trend_model is not None
    except Exception as e:
        st.error(f"SYSTEM ERROR: Model/Data Loading Failed: {str(e)}")
        models_loaded = False

    if models_loaded:
        def rebuild_target(row):
            if row["Target_Graduate"] == 1:
                return "Graduate"
            elif row["Target_Enrolled"] == 1:
                return "Enrolled"
            else:
                return "Dropout"


        df["Grade"] = df.apply(rebuild_target, axis=1)

        # Plotly Theme
        PLOT_THEME = dict(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', family="Inter"),
            colorway=['#00f2ff', '#bc13fe', '#0aff60', '#ff0055']
        )

        # --- TABS ---
        if role == "student":
            tab1, tab2, tab3 = st.tabs(["🔮 PREDICTION ENGINE", "📊 PERFORMANCE ANALYTICS", "📚 RECOMMENDATION HUB"])
        elif role == "teacher":
            tab1, tab2, tab3 = st.tabs(["👥 CLASSROOM ANALYSIS", "📈 TREND METRICS", "🚨 RISK MONITOR"])
        else:
            tab1, tab2, tab3 = st.tabs(["🔍 DIAGNOSTIC TOOL", "📊 INSTITUTIONAL DATA", "🎯 INTERVENTION PLAN"])

        # --- TAB 1 CONTENT ---
        with tab1:
            # Role Specific Inputs
            col_left, col_right = st.columns([1, 1.5])

            with col_left:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:{current_color}; margin-bottom: 1.5rem;'>/// INPUT PARAMETERS</h3>",
                            unsafe_allow_html=True)

                # Inputs depending on role
                if role == "student":
                    age = st.slider("MY AGE", 17, 60, 22)
                    admission_grade = st.slider("ADMISSION SCORE", 0.0, 200.0, 120.0)
                    gender = st.selectbox("GENDER IDENTITY", ["male", "female"])
                    scholarship = st.selectbox("SCHOLARSHIP STATUS", ["yes", "no"])
                    tuition_paid = st.selectbox("TUITION STATUS", ["yes", "no"])
                    sem1_grade = st.slider("SEM 1 GPA", 0.0, 20.0, 12.0)
                    sem2_grade = st.slider("SEM 2 GPA", 0.0, 20.0, 12.0)
                else:  # Teacher & Counselor share similar input sliders for students
                    age = st.slider("STUDENT AGE", 17, 60, 22)
                    admission_grade = st.slider("ADMISSION SCORE", 0.0, 200.0, 120.0)
                    gender = st.selectbox("GENDER", ["male", "female"])
                    scholarship = st.selectbox("SCHOLARSHIP", ["yes", "no"])
                    tuition_paid = st.selectbox("TUITION PAID", ["yes", "no"])
                    sem1_grade = st.slider("SEM 1 GRADE", 0.0, 20.0, 12.0)
                    sem2_grade = st.slider("SEM 2 GRADE", 0.0, 20.0, 12.0)

                # Common inputs
                unemployment = st.slider("UNEMPLOYMENT INDEX", 0.0, 20.0, 7.5)
                inflation = st.slider("INFLATION INDEX", 0.0, 10.0, 3.0)
                gdp = st.slider("GDP INDEX", 0.0, 200000.0, 100000.0)

                # Model Selector
                if available_models:
                    with st.expander("⚙️ SYSTEM CONFIGURATION"):
                        selected_model_name = st.selectbox("AI MODEL", list(available_models.keys()))
                    selected_model = available_models[selected_model_name]

                st.markdown("<br>", unsafe_allow_html=True)
                analyze_btn = st.button("INITIATE ANALYSIS PROCESS", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_right:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:{current_color}; margin-bottom: 1.5rem;'>/// DIAGNOSTIC OUTPUT</h3>",
                            unsafe_allow_html=True)

                if analyze_btn:
                    # Prediction Logic
                    base_input = df.drop(columns=[col for col in df.columns if "Target" in col or col == "Grade"])
                    model_columns = base_input.columns.tolist()
                    input_template = pd.DataFrame(columns=model_columns)
                    defaults = {}
                    for col in model_columns:
                        try:
                            if pd.api.types.is_numeric_dtype(df[col]):
                                defaults[col] = float(df[col].median())
                            else:
                                mode_series = df[col].mode()
                                defaults[col] = mode_series.iloc[0] if not mode_series.empty else df[col].iloc[0]
                        except Exception:
                            defaults[col] = 0
                    input_template.loc[0] = defaults

                    input_template["Age at enrollment"] = age
                    input_template["Admission grade"] = admission_grade
                    input_template["Gender"] = 1 if gender == "male" else 0
                    input_template["Scholarship holder"] = 1 if scholarship == "yes" else 0
                    input_template["Tuition fees up to date"] = 1 if tuition_paid == "yes" else 0
                    input_template["Curricular units 1st sem (grade)"] = sem1_grade
                    input_template["Curricular units 2nd sem (grade)"] = sem2_grade
                    input_template["Unemployment rate"] = unemployment
                    input_template["Inflation rate"] = inflation
                    input_template["GDP"] = gdp

                    # Ensure correct columns
                    input_template = input_template[model_columns]

                    # Clean types
                    for col in input_template.columns:
                        if pd.api.types.is_integer_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
                            input_template[col] = np.round(input_template[col]).astype(df[col].dtype)

                    prediction = selected_model.predict(input_template)[0]
                    probabilities = selected_model.predict_proba(input_template)[0]
                    confidence = round(probabilities[prediction] * 100, 2)
                    label_map = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
                    result = label_map[prediction]

                    sem2_pred = trend_model.predict([[sem1_grade]])[0]
                    is_anomaly = anomaly_model.predict(input_template)[0] == -1

                    # Dynamic Result Styling based on Prediction
                    if result == "Dropout":
                        border_color = "#ff0055"
                        status_text = "RISK ALERT"
                        status_description = {
                            "student": "Your profile indicates significant academic challenges. Immediate consultation with a counselor is vital to prevent drop-out.",
                            "teacher": f"This student requires high-priority academic support. Key risk factors: Low Grades (Sem 2 Pred: {round(sem2_pred, 2)}) and potential financial/economic stress.",
                            "counselor": "Trigger Tier 1 intervention protocol. Focus on root causes (financial aid, mental health, or academic skill deficits)."
                        }.get(role, "High risk of attrition detected.")
                    elif result == "Graduate":
                        border_color = "#0aff60"
                        status_text = "SUCCESS LIKELY"
                        status_description = {
                            "student": "Your path to graduation is strong! Keep maintaining excellent academic and financial standing. Explore career services next.",
                            "teacher": f"Strong performer. Maintain standard engagement. Next Sem Grade: {round(sem2_pred, 2)}. Consider for advanced placement or mentoring roles.",
                            "counselor": "Student is on track. Mark for Tier 3 (Success) monitoring. Ensure transition to alumni/career services is smooth."
                        }.get(role, "Student predicted to successfully graduate.")
                    else:  # Enrolled (Default state)
                        border_color = "#f59e0b"
                        status_text = "ON TRACK"
                        status_description = {
                            "student": "You are currently maintaining a stable academic path. Focus on continuous improvement and utilize campus resources.",
                            "teacher": f"Stable performance. Next Sem Grade: {round(sem2_pred, 2)}. Requires standard monitoring. Low risk of immediate failure.",
                            "counselor": "Student is stable (Tier 2). Recommend proactive check-ins to optimize performance and prevent minor deviations."
                        }.get(role, "Student predicted to continue enrollment.")

                    glow_color = f"{border_color}40"

                    # Output Card HTML
                    st.markdown(f"""
                    <div class='result-card-glass' style='border-left-color: {border_color}; box-shadow: 0 0 30px {glow_color};'>
                        <h4 style='color: #aaa; letter-spacing: 2px; margin:0;'>{status_text}</h4>
                        <h1 style='font-size: 3.5rem; margin: 10px 0; color: {border_color}; text-shadow: 0 0 10px {border_color};'>{result.upper()}</h1>
                        <p style='color: #ddd; margin-bottom: 20px;'>{status_description}</p>
                        <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
                            <div>
                                <small style='color: #888;'>CONFIDENCE</small>
                                <h3 style='margin:0;'>{confidence}%</h3>
                            </div>
                            <div style='border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px;'>
                                <small style='color: #888;'>NEXT SEM GPA</small>
                                <h3 style='margin:0;'>{round(sem2_pred, 2)}</h3>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- NEW: PROFILE RADAR ANALYSIS ---
                    col_radar, col_metrics = st.columns([1.5, 1])

                    with col_radar:
                        st.markdown("##### 📡 PROFILE RADAR ANALYSIS")
                        categories = ['Admission', 'Sem 1', 'Sem 2', 'Unemployment', 'GDP Impact']

                        # Normalize values roughly for visualization (0-1 scale approximation)
                        vals = [
                            min(admission_grade / 200, 1),
                            min(sem1_grade / 20, 1),
                            min(sem2_grade / 20, 1),
                            1 - min(unemployment / 20, 1),  # Inverted because lower is better
                            min(gdp / 200000, 1)
                        ]

                        # Prepare proper rgba string for Plotly fillcolor
                        hex_c = current_color.lstrip('#')
                        rgb_vals = tuple(int(hex_c[i:i + 2], 16) for i in (0, 2, 4))
                        rgba_color = f"rgba({rgb_vals[0]}, {rgb_vals[1]}, {rgb_vals[2]}, 0.3)"

                        fig_radar = go.Figure()
                        fig_radar.add_trace(go.Scatterpolar(
                            r=vals,
                            theta=categories,
                            fill='toself',
                            name='Student Profile',
                            line_color=current_color,
                            fillcolor=rgba_color
                        ))

                        # Add a hypothetical "Average Success" baseline
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[0.7, 0.65, 0.65, 0.8, 0.6],
                            theta=categories,
                            fill='toself',
                            name='Class Baseline',
                            line_color='#444',
                            opacity=0.5
                        ))

                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
                                bgcolor='rgba(0,0,0,0)'
                            ),
                            showlegend=False,
                            margin=dict(t=20, b=20, l=20, r=20),
                            height=250,
                            **PLOT_THEME
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)

                    with col_metrics:
                        st.markdown("##### 🔑 KEY INDICATORS")
                        st.markdown(f"""
                        <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px;'>
                            <small style='color:#888'>SCHOLARSHIP</small><br>
                            <span style='color: {"#0aff60" if scholarship == "yes" else "#ff0055"}'>
                                {'ACTIVE' if scholarship == "yes" else 'INACTIVE'}
                            </span>
                        </div>
                        <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px;'>
                            <small style='color:#888'>TUITION</small><br>
                            <span style='color: {"#0aff60" if tuition_paid == "yes" else "#ff0055"}'>
                                {'PAID' if tuition_paid == "yes" else 'PENDING'}
                            </span>
                        </div>
                        <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px;'>
                            <small style='color:#888'>ECONOMIC CONTEXT</small><br>
                            <span style='color: #00f2ff'>
                                {'HIGH GROWTH' if gdp > 120000 else 'STABLE'}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                    if is_anomaly:
                        st.markdown(
                            "<div style='margin-top:15px; padding:10px; background:rgba(255,0,85,0.2); border:1px solid #ff0055; border-radius:8px; color:#ffb3c6; text-align:center;'>⚠️ ANOMALY DETECTED: DATA PATTERN IRREGULAR</div>",
                            unsafe_allow_html=True)

                    # Detailed Report Content
                    report_txt = f"""
=============================================================
       🎓 EDUPREDICT | ACADEMIC INTELLIGENCE REPORT
=============================================================

[REPORT METADATA]
-------------------------------------------------------------
Generated By:       {role.upper()}
Date:               {datetime.now().strftime('%Y-%m-%d')}
Time:               {datetime.now().strftime('%H:%M:%S')}
System Version:     v{APP_VERSION}

[STUDENT PROFILE]
-------------------------------------------------------------
Age at Enrollment:  {age}
Admission Grade:    {admission_grade}
Gender:             {gender.capitalize()}
Scholarship:        {scholarship.capitalize()}
Tuition Status:     {'Paid' if tuition_paid == 'yes' else 'Unpaid'}
Sem 1 Grade:        {sem1_grade}
Sem 2 Grade:        {sem2_grade}

[ECONOMIC CONTEXT]
-------------------------------------------------------------
Unemployment Rate:  {unemployment}%
Inflation Rate:     {inflation}%
GDP Index:          {gdp}

[ANALYSIS RESULTS]
-------------------------------------------------------------
Predicted Outcome:  {result.upper()}
Confidence Score:   {confidence}%
Anomaly Detected:   {'YES' if is_anomaly else 'NO'}
Next Sem Forecast:  {round(sem2_pred, 2)} (Estimated)

[INTERVENTION NOTE]
-------------------------------------------------------------
This report is generated by an AI model. The predictions
are advisory. Please consult with academic counselors for
authorized support plans.

=============================================================
© 2024 EduPredict Systems. All Rights Reserved.
=============================================================
"""
                    st.download_button("DOWNLOAD FULL REPORT", report_txt, file_name="edu_predict_report.txt",
                                       use_container_width=True)

                else:
                    st.info("Awaiting Input Parameters...")
                    st.markdown("<div style='text-align:center; opacity:0.3; font-size:5rem;'>📊</div>",
                                unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # --- QUICK PREDICT ACADEMIC OUTCOME ---
            st.markdown("---")
            st.markdown(
                f"<h3 style='color: {current_color}; text-align: center;'>/// QUICK PREDICT ACADEMIC OUTCOME</h3>",
                unsafe_allow_html=True)
            st.markdown(
                "<p style='text-align: center; color: #888;'>Alternative simulation tool for quick assessments.</p>",
                unsafe_allow_html=True)

            with st.container():
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

                # MODEL SELECTOR FOR QUICK PREDICT
                if available_models:
                    col_q1, col_q2 = st.columns([1, 2])
                    with col_q1:
                        quick_model_name = st.selectbox("SELECT SIMULATION MODEL", list(available_models.keys()),
                                                        key="quick_model")
                        quick_model = available_models[quick_model_name]
                    with col_q2:
                        st.empty()  # Spacer

                st.markdown("<br>", unsafe_allow_html=True)

                # FULL INPUT GRID (5 Columns x 2 Rows)
                c1, c2, c3, c4, c5 = st.columns(5)

                with c1:
                    gen_age = st.slider("Age", 17, 60, 22, key="gen_age")
                    gen_sem1 = st.slider("Sem 1 Grade", 0.0, 20.0, 12.0, key="gen_s1")
                with c2:
                    gen_adm = st.slider("Adm. Grade", 0.0, 200.0, 120.0, key="gen_adm")
                    gen_sem2 = st.slider("Sem 2 Grade", 0.0, 20.0, 12.0, key="gen_s2")
                with c3:
                    gen_gender = st.selectbox("Gender", ["male", "female"], key="gen_gen")
                    gen_unemp = st.slider("Unemployment", 0.0, 20.0, 7.5, key="gen_un")
                with c4:
                    gen_schol = st.selectbox("Scholarship", ["yes", "no"], key="gen_sch")
                    gen_inf = st.slider("Inflation", 0.0, 10.0, 3.0, key="gen_inf")
                with c5:
                    gen_tuit = st.selectbox("Tuition", ["yes", "no"], key="gen_tui")
                    gen_gdp = st.slider("GDP", 0.0, 200000.0, 100000.0, key="gen_gdp")

                st.markdown("<br>", unsafe_allow_html=True)
                gen_btn = st.button("🚀 RUN QUICK SIMULATION", use_container_width=True, key="gen_btn")

                if gen_btn:
                    # Use selected quick model
                    model_to_use = quick_model if 'quick_model' in locals() else available_models[
                        list(available_models.keys())[0]]

                    base_cols = df.drop(columns=[c for c in df.columns if "Target" in c or c == "Grade"]).columns
                    gen_input = pd.DataFrame(columns=base_cols)
                    defaults = {}
                    for col in base_cols:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            defaults[col] = df[col].median()
                        else:
                            defaults[col] = df[col].mode()[0]
                    gen_input.loc[0] = defaults

                    # Map all inputs
                    gen_input["Age at enrollment"] = gen_age
                    gen_input["Admission grade"] = gen_adm
                    gen_input["Gender"] = 1 if gen_gender == "male" else 0
                    gen_input["Scholarship holder"] = 1 if gen_schol == "yes" else 0
                    gen_input["Tuition fees up to date"] = 1 if gen_tuit == "yes" else 0
                    gen_input["Curricular units 1st sem (grade)"] = gen_sem1
                    gen_input["Curricular units 2nd sem (grade)"] = gen_sem2
                    gen_input["Unemployment rate"] = gen_unemp
                    gen_input["Inflation rate"] = gen_inf
                    gen_input["GDP"] = gen_gdp

                    # Clean types
                    for col in gen_input.columns:
                        if pd.api.types.is_integer_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
                            gen_input[col] = np.round(gen_input[col]).astype(df[col].dtype)

                    gen_pred = model_to_use.predict(gen_input)[0]
                    gen_conf = round(model_to_use.predict_proba(gen_input)[0][gen_pred] * 100, 2)
                    gen_res = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}[gen_pred]
                    color_res = "#ff0055" if gen_res == "Dropout" else "#0aff60" if gen_res == "Graduate" else "#f59e0b"

                    st.markdown(f"""
                    <div style='margin-top: 20px; padding: 15px; border: 1px solid {color_res}; background: {color_res}20; border-radius: 10px; text-align: center;'>
                        <h2 style='margin:0; color: {color_res};'>PREDICTION: {gen_res.upper()}</h2>
                        <p style='margin:0; color: white;'>Confidence: {gen_conf}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # --- TAB 2: ANALYTICS ---
        with tab2:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 📊 PERFORMANCE METRICS", unsafe_allow_html=True)

                if role == "student":
                    chart_opts = ["My Performance vs Peers", "Grade Trends", "Success Probability"]
                else:
                    chart_opts = ["Class Distribution", "Performance Trends", "Risk Assessment"]

                chart_type = st.selectbox("SELECT VISUALIZATION", chart_opts)

                if "Distribution" in chart_type or "Peers" in chart_type:
                    fig = px.pie(df, names="Grade", hole=0.5, color_discrete_sequence=PLOT_THEME['colorway'])
                    fig.update_layout(**PLOT_THEME)
                    st.plotly_chart(fig, use_container_width=True)
                elif "Trends" in chart_type:
                    fig = px.line(
                        df[["Curricular units 1st sem (grade)", "Curricular units 2nd sem (grade)"]].reset_index().head(
                            100),
                        color_discrete_sequence=PLOT_THEME['colorway'])
                    fig.update_layout(**PLOT_THEME)
                    st.plotly_chart(fig, use_container_width=True)
                elif "Probability" in chart_type or "Risk" in chart_type:
                    fig = px.box(df, x="Grade", y="Admission grade", color="Grade",
                                 color_discrete_sequence=PLOT_THEME['colorway'])
                    fig.update_layout(**PLOT_THEME)
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### ⚡ DATA INSIGHTS", unsafe_allow_html=True)
                st.metric("TOTAL RECORDS", df.shape[0])
                st.metric("SUCCESS RATE", f"{len(df[df['Grade'] == 'Graduate']) / len(df) * 100:.1f}%", delta="1.2%")
                st.metric("RISK FACTOR", f"{len(df[df['Grade'] == 'Dropout']) / len(df) * 100:.1f}%", delta="-0.5%",
                          delta_color="inverse")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🧠 AI CORRELATION", unsafe_allow_html=True)
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) > 1:
                    corr = df[numeric_cols].corr().iloc[:5, :5]
                    fig_corr = px.imshow(corr, color_continuous_scale="RdBu_r")
                    fig_corr.update_layout(margin=dict(l=0, r=0, t=0, b=0), **PLOT_THEME)
                    st.plotly_chart(fig_corr, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # --- TAB 3: RECOMMENDATION HUB (RESTYLED) ---
        with tab3:
            if role == "student":
                col_r1, col_r2 = st.columns([2, 1])
                with col_r1:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{current_color};'>📚 PERSONALIZED STUDY STRATEGY</h3>",
                                unsafe_allow_html=True)
                    st.markdown("""
                    <div class='rec-card'>
                        <div class='rec-header'>🧠 COGNITIVE OPTIMIZATION</div>
                        <p>• Focus on improving your weakest subjects by allocating 20% more time.</p>
                        <p>• Create a study schedule and stick to it to build consistency.</p>
                    </div>
                    <div class='rec-card' style='border-color: #bc13fe;'>
                        <div class='rec-header' style='color: #bc13fe;'>🤝 COLLABORATIVE LEARNING</div>
                        <p>• Join study groups for 'Programming I' to enhance problem-solving.</p>
                        <p>• Use active learning techniques like teaching concepts to peers.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_r2:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{current_color};'>📈 SUCCESS METRICS</h3>", unsafe_allow_html=True)
                    st.markdown("""
                    <div class='story-card'>
                        <span>✅</span> <span>Similar profiles achieved 85% success rate</span>
                    </div>
                    <div class='story-card'>
                        <span>📅</span> <span>Regular attendance boosts grades by 15%</span>
                    </div>
                    <div class='story-card'>
                        <span>🚀</span> <span>Early help prevents 60% of failures</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Resources Strip
                st.markdown(f"""
                <div class='glass-card' style='display:flex; justify-content:space-around; text-align:center;'>
                    <div>📖<br>Academic Support</div>
                    <div>🧠<br>Mental Health</div>
                    <div>💰<br>Financial Aid</div>
                    <div>🎯<br>Career Center</div>
                </div>
                """, unsafe_allow_html=True)

            elif role == "teacher":
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{current_color};'>🚨 RISK ALERTS</h3>", unsafe_allow_html=True)
                    high_risk = df[df['Grade'] == 'Dropout']
                    st.warning(f"⚠️ **{len(high_risk)} students identified as high-risk**")
                    if len(high_risk) > 0:
                        st.dataframe(high_risk[['Age at enrollment', 'Admission grade',
                                                'Curricular units 1st sem (grade)']].head(5), use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_t2:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{current_color};'>📊 INTERVENTION IMPACT</h3>",
                                unsafe_allow_html=True)
                    st.markdown("""
                    <div class='rec-card'>
                        <div class='rec-header'>EARLY WARNING SYSTEM</div>
                        <p>Improves success rate by 40% when acted upon within 2 weeks.</p>
                    </div>
                    <div class='rec-card' style='border-color: #0aff60;'>
                        <div class='rec-header' style='color: #0aff60;'>PERSONALIZED SUPPORT</div>
                        <p>Plans increase retention by 30% for at-risk demographics.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            else:  # Counselor
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{current_color};'>🎯 STRATEGIC FRAMEWORK</h3>",
                                unsafe_allow_html=True)
                    st.markdown("""
                    <div class='rec-card' style='border-color: #ff0055;'>
                        <div class='rec-header' style='color: #ff0055;'>TIER 1: HIGH RISK</div>
                        <p>Immediate 1-on-1 counseling and financial review required.</p>
                    </div>
                    <div class='rec-card' style='border-color: #f59e0b;'>
                        <div class='rec-header' style='color: #f59e0b;'>TIER 2: PREVENTIVE</div>
                        <p>Regular monitoring and study skills workshops.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_c2:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{current_color};'>📈 INSTITUTIONAL GOALS</h3>",
                                unsafe_allow_html=True)
                    c_a, c_b = st.columns(2)
                    c_a.metric("Retention Goal", "85%", "5%")
                    c_b.metric("Avg GPA Target", "14.0", "0.5")
                    st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("SYSTEM ERROR: MODELS NOT LOADED")
        st.code("Please verify 'data/' and 'models/' directories.")

# --- FOOTER ---
st.markdown(f"""
<div class='footer'>
    <p>Made with ❤️ by EduPredict | <a href='https://forms.gle/dEW6AfgRSia92J438'>FEEDBACK FORM</a> | <a href='#'>SYSTEM STATUS</a> | v{APP_VERSION}</p>
</div>
""", unsafe_allow_html=True)