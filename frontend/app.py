import streamlit as st
import requests

st.set_page_config(page_title="YouTube Predictor", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>

/* FULL PAGE BACKGROUND */
body {
    background: radial-gradient(circle at 20% 20%, #1e3a8a, transparent 40%),
                radial-gradient(circle at 80% 30%, #9333ea, transparent 40%),
                radial-gradient(circle at 50% 80%, #0ea5e9, transparent 40%),
                linear-gradient(135deg, #020617, #020617);
    background-attachment: fixed;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 44px;
    font-weight: bold;
    color: #f8fafc;
    text-shadow: 0 0 20px rgba(99,102,241,0.6);
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: #cbd5f5;
    margin-bottom: 30px;
}

/* GLASS CARD */
.card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(20px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 0px 40px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
}

/* RESULT HIGH */
.result-high {
    background: linear-gradient(90deg, #065f46, #10b981);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 22px;
    box-shadow: 0 0 20px rgba(16,185,129,0.6);
}

/* RESULT LOW */
.result-low {
    background: linear-gradient(90deg, #7f1d1d, #ef4444);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 22px;
    box-shadow: 0 0 20px rgba(239,68,68,0.6);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(147,51,234,0.7);
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">🎬 YouTube Success Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict virality before you upload 🚀</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

title = st.text_input("🎯 Enter Video Title")

predict = st.button("🚀 Analyze")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- LOGIC ----------
if predict:
    if title.strip() == "":
        st.warning("Enter a valid title")
    else:
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/predict",
                    params={"title": title}
                )
                result = res.json()

                st.markdown("---")

                # ---------- RESULT ----------
                if result["prediction"] == "HIGH":
                    st.markdown(
                        '<div class="result-high">🔥 HIGH VIRAL POTENTIAL</div>',
                        unsafe_allow_html=True
                    )
                    st.progress(85)
                    st.balloons()

                else:
                    st.markdown(
                        '<div class="result-low">⚠️ LOW VIRAL POTENTIAL</div>',
                        unsafe_allow_html=True
                    )
                    st.progress(30)

                # ---------- INSIGHTS ----------
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📊 Title Analysis")
                    st.write(f"Length: {len(title)} characters")
                    st.write(f"Words: {len(title.split())}")

                with col2:
                    st.markdown("### 💡 Suggestions")
                    st.write("✔ Add numbers (Top 5, 10 Tips)")
                    st.write("✔ Use emotional triggers")
                    st.write("✔ Keep under 10 words")

            except:
                st.error("Backend not running")