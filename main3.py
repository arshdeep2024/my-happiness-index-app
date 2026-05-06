import streamlit as st
import torch
import os
import base64

# =====================================================
# PERFORMANCE
# =====================================================
torch.set_num_threads(2)

# =====================================================
# IMPORT BACKEND
# =====================================================
from ayush_drive import (
    QUESTIONS,
    process_text_answer
)

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GIF_DIR = os.path.join(BASE_DIR, "gifs")

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Interactive Feedback System",
    layout="centered"
)

# =====================================================
# GIF DISPLAY
# =====================================================
def show_gif(filename, width=260):

    path = os.path.join(GIF_DIR, filename)

    if os.path.exists(path):

        with open(path, "rb") as f:
            data = f.read()

        b64 = base64.b64encode(data).decode()

        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="data:image/gif;base64,{b64}" width="{width}">
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# FINAL GIF
# =====================================================
def final_gif(score):

    val = score * 100

    if val < 30:
        return "anger.gif"

    elif val < 40:
        return "sad.gif"

    elif val < 60:
        return "neutral.gif"

    else:
        return "happy.gif"

# =====================================================
# SESSION STATE
# =====================================================
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "hi_scores" not in st.session_state:
    st.session_state.hi_scores = []

if "completed" not in st.session_state:
    st.session_state.completed = False

# =====================================================
# TITLE
# =====================================================
st.title("AI-Powered Interactive Feedback System 🌱")

# =====================================================
# HOME PAGE
# =====================================================
if st.session_state.current_q == 0 and not st.session_state.completed:

    show_gif("speaking.gif")

    st.markdown(
        """
        ### Answer 2 quick questions and let AI analyze your response.
        """
    )

    if st.button("START FEEDBACK"):

        st.session_state.current_q = 1
        st.rerun()

    st.stop()

# =====================================================
# FINAL RESULT PAGE
# =====================================================
if st.session_state.completed:

    final_hi = st.session_state.hi_scores[0]

    st.markdown("## You seem")

    show_gif(final_gif(final_hi), width=320)

    st.markdown("## with our project")

    st.markdown("### Thanks for the feedback 🌱")

    if st.button("Give Another Feedback"):

        st.session_state.current_q = 0
        st.session_state.hi_scores = []
        st.session_state.completed = False

        st.rerun()

    st.stop()

# =====================================================
# QUESTIONS
# =====================================================
q = st.session_state.current_q - 1

show_gif("surprise.gif")

st.write(f"Question {q+1} of {len(QUESTIONS)}")

st.subheader(QUESTIONS[q])

answer = st.text_area(
    "Your Answer",
    key=f"textbox_{q}"
)

# =====================================================
# SUBMIT
# =====================================================
if st.button("Submit Answer"):

    if answer.strip() == "":
        st.warning("Please enter an answer.")
        st.stop()

    with st.spinner("Processing..."):

        hi = process_text_answer(answer)

    # Only FIRST question contributes to HI
    if q == 0:
        st.session_state.hi_scores.append(hi)

    st.session_state.current_q += 1

    if st.session_state.current_q > len(QUESTIONS):
        st.session_state.completed = True

    st.rerun()