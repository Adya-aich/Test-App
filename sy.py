import streamlit as st
import math

# ------------------------------
# Page setup
# ------------------------------
st.set_page_config(page_title="Casio FX-991 | Scientific Calculator", page_icon="🧮", layout="centered")

# ------------------------------
# Custom CSS (for better UI)
# ------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #111;
        color: white;
        text-align: center;
    }
    .stTextInput>div>div>input {
        text-align: right;
        font-size: 24px !important;
        color: #00FFAA !important;
        background-color: #000 !important;
        border: 2px solid #444 !important;
        border-radius: 8px;
        height: 60px !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #222;
        color: white;
        border: 1px solid #555;
        border-radius: 8px;
        height: 50px;
        width: 75px;
        font-size: 18px;
        font-weight: 600;
        margin: 3px;
    }
    .stButton>button:hover {
        background-color: #444;
        border-color: #777;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Session State
# ------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------
# Core Functions
# ------------------------------
def add_symbol(symbol):
    st.session_state.expression += symbol

def clear_display():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def evaluate_expression():
    expr = st.session_state.expression
    try:
        expr = expr.replace("^", "**")
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))
        expr = expr.replace("√", "math.sqrt")
        result = eval(expr, {"__builtins__": None}, math.__dict__)
        st.session_state.history.append(f"{st.session_state.expression} = {result}")
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Error"

# ------------------------------
# Title and Display
# ------------------------------
st.markdown("<h2>🧮 Casio FX-991 Scientific Calculator</h2>", unsafe_allow_html=True)
st.text_input("Display", value=st.session_state.expression, key="display", disabled=True)

# ------------------------------
# Button Layout (Casio Style)
# ------------------------------
buttons = [
    ["(", ")", "π", "e", "C"],
    ["7", "8", "9", "/", "sin("],
    ["4", "5", "6", "*", "cos("],
    ["1", "2", "3", "-", "tan("],
    ["0", ".", "^", "+", "="],
    ["log(", "ln(", "√(", "!", "⌫"]
]

# ------------------------------
# Render Buttons
# ------------------------------
for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        with cols[i]:
            if st.button(btn):
                if btn == "C":
                    clear_display()
                elif btn == "=":
                    evaluate_expression()
                elif btn == "⌫":
                    backspace()
                elif btn == "!":
                    try:
                        val = int(st.session_state.expression)
                        st.session_state.expression = str(math.factorial(val))
                    except Exception:
                        st.session_state.expression = "Error"
                else:
                    add_symbol(btn)
    st.write("")

# ------------------------------
# History Section
# ------------------------------
if st.session_state.history:
    st.markdown("### 🧾 Recent Calculations")
    for h in reversed(st.session_state.history[-5:]):
        st.text(h)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Made with ❤️ using Streamlit | Casio FX-991 Replica")
