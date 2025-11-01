import streamlit as st
import math

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="Casio FX-991 | Scientific Calculator", page_icon="🧮", layout="centered")

# -----------------------------
# Custom CSS for UI Styling
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #1b1b1b;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background-color: #333;
        color: white;
        border: 1px solid #555;
        border-radius: 8px;
        height: 50px;
        width: 80px;
        font-size: 18px;
        font-weight: 600;
        margin: 3px;
    }
    .stButton>button:hover {
        background-color: #555;
        border-color: #888;
    }
    input[disabled] {
        color: #00FFAA !important;
        font-weight: bold;
        font-size: 22px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Initialize session state
# -----------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Helper functions
# -----------------------------
def append(symbol):
    st.session_state.expression += symbol

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def evaluate():
    expr = st.session_state.expression
    try:
        expr = expr.replace("^", "**")
