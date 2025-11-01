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
        # Replace math functions with python equivalents
        expr = expr.replace("^", "**")
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))
        expr = expr.replace("√", "math.sqrt")
        result = eval(expr, {"__builtins__": None}, math.__dict__)
        st.session_state.history.append(f"{st.session_state.expression} = {result}")
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Error"

# -----------------------------
# Display
# -----------------------------
st.markdown("## 🧮 Casio FX-991 Scientific Calculator")

# Display screen
st.text_input("Display", value=st.session_state.expression, key="display", disabled=True)

# -----------------------------
# Button Layout
# -----------------------------
buttons = [
    ["(", ")", "π", "e", "C"],
    ["7", "8", "9", "/", "sin("],
    ["4", "5", "6", "*", "cos("],
    ["1", "2", "3", "-", "tan("],
    ["0", ".", "^", "+", "="],
    ["log(", "ln(", "√(",]()
