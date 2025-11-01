# app.py
import streamlit as st
import math
import re

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="Casio FX-991 | Scientific Calculator", page_icon="🧮", layout="centered")

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #0f1724; color: #e6eef8; }
    .calculator-title { text-align: center; margin-bottom: 10px; }
    .stTextInput>div>div>input { 
        text-align: right; font-size: 24px !important; color: #8ef0c2 !important;
        background-color: #071024 !important; border: 2px solid #233240 !important;
        border-radius: 8px; height: 60px !important; font-weight: 700;
    }
    .stButton>button {
        background-color: #0b2b3a; color: #e6eef8; border: 1px solid #234455;
        border-radius: 10px; height: 54px; width: 78px; font-size: 18px; font-weight: 700;
    }
    .stButton>button:hover { background-color: #144055; border-color: #2b6a88; }
    .small { font-size:13px; color:#9fb6c8 }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session state
# -----------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "angle_mode" not in st.session_state:
    st.session_state.angle_mode = "DEG"  # or "RAD"

# -----------------------------
# Helper functions and safe eval
# -----------------------------

def append(symbol: str):
    st.session_state.expression += symbol

def clear_display():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def to_float_if_possible(x):
    try:
        return float(x)
    except Exception:
        return x

# wrappers for trig that respect DEG/RAD mode
def _sin(x):
    x = to_float_if_possible(x)
    if st.session_state.angle_mode == "DEG":
        return math.sin(math.radians(x))
    return math.sin(x)

def _cos(x):
    x = to_float_if_possible(x)
    if st.session_state.angle_mode == "DEG":
        return math.cos(math.radians(x))
    return math.cos(x)

def _tan(x):
    x = to_float_if_possible(x)
    if st.session_state.angle_mode == "DEG":
        return math.tan(math.radians(x))
    return math.tan(x)

def _asin(x):
    val = math.asin(x)
    if st.session_state.angle_mode == "DEG":
        return math.degrees(val)
    return val

def _acos(x):
    val = math.acos(x)
    if st.session_state.angle_mode == "DEG":
        return math.degrees(val)
    return val

def _atan(x):
    val = math.atan(x)
    if st.session_state.angle_mode == "DEG":
        return math.degrees(val)
    return val

def _fact(x):
    # support only non-negative integers like Casio (raise error otherwise)
    try:
        n = int(x)
        if n < 0:
            raise ValueError("Factorial only defined for non-negative integers")
        return math.factorial(n)
    except Exception as e:
        raise

# Allowed names for eval
SAFE_NAMES = {
    # constants
    "pi": math.pi,
    "π": math.pi,
    "e": math.e,
    # basic math
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    # logs
    "log": lambda x: math.log10(x),
    "ln": math.log,
    # power
    "pow": pow,
    # trig wrappers
    "sin": _sin,
    "cos": _cos,
    "tan": _tan,
    "asin": _asin,
    "acos": _acos,
    "atan": _atan,
    # factorial
    "fact": _fact,
    # math module helpers (if needed)
    "floor": math.floor,
    "ceil": math.ceil,
}

# sanitize and prepare expression before eval
def prepare_expression(expr: str) -> str:
    # Replace unicode sqrt symbol with function name
    expr = expr.replace("√", "sqrt")
    # Replace caret with python power
    expr = expr.replace("^", "**")
    # Allow user-friendly factorial: convert trailing "!" to fact(...)
    # e.g. "5!" -> "fact(5)"; handle chained or parenthesized expressions like (3+2)!
    # This uses a simple regex to find occurrences of something followed by !
    # We'll repeatedly replace until no '!' left (handles nested)
    # Pattern: capture a number or closing paren or identifier
    while "!" in expr:
        # Try to replace the last occurrence to keep parentheses correct
        # regex finds the rightmost occurrence of (<expr>)! or number!
        m = re.search(r"(?P<inside>(?:\d+\.?\d*|\([^\)]+\)|[A-Za-z_][A-Za-z0-9_]*))\!", expr)
        if not m:
            # if weird pattern, break to avoid infinite loop
            break
        inside = m.group("inside")
        start, end = m.span()
        expr = expr[:start] + f"fact({inside})" + expr[end:]
    # Remove accidental repeated characters (optional safety)
    return expr

def evaluate_expression():
    expr = st.session_state.expression.strip()
    if not expr:
        return
    try:
        expr_prepared = prepare_expression(expr)
        # Evaluate in restricted namespace
        result = eval(expr_prepared, {"__builtins__": None}, SAFE_NAMES)
        # Format result: if it's a float and close to int, show int
        if isinstance(result, float) and abs(result - round(result)) < 1e-12:
            result = round(result)
        st.session_state.history.append(f"{expr} = {result}")
        st.session_state.expression = str(result)
    except Exception as e:
        # Put a friendly error message on screen
        st.session_state.expression = "Error"

# -----------------------------
# UI
# -----------------------------
st.markdown('<div class="calculator-title"><h2>🧮 Casio FX-991 — Scientific Calculator</h2></div>', unsafe_allow_html=True)

# Angle mode toggle
col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("DEG") and st.session_state.angle_mode != "DEG":
        st.session_state.angle_mode = "DEG"
with col_b:
    if st.button("RAD") and st.session_state.angle_mode != "RAD":
        st.session_state.angle_mode = "RAD"

st.write(f"**Mode:** {st.session_state.angle_mode}")

# Display (disabled input)
st.text_input("Display", value=st.session_state.expression, key="display", disabled=True)

# Buttons layout (rows)
buttons = [
    ["(", ")", "π", "e", "C"],
    ["7", "8", "9", "/", "sin("],
    ["4", "5", "6", "*", "cos("],
    ["1", "2", "3", "-", "tan("],
    ["0", ".", "^", "+", "="],
    ["log(", "ln(", "√(", "!", "⌫"]
]

# Render buttons
for row in buttons:
    cols = st.columns(len(row))
    for i, button_label in enumerate(row):
        with cols[i]:
            if st.button(button_label):
                if button_label == "C":
                    clear_display()
                elif button_label == "=":
                    evaluate_expression()
                elif button_label == "⌫":
                    backspace()
                elif button_label == "!":
                    # If user pressed '!' button, append '!' so prepare_expression converts it to fact(...)
                    append("!")
                else:
                    # For π show the symbol for replacement (prepare_expression handles "π")
                    append(button_label)
    st.write("")

# History panel (last 8)
if st.session_state.history:
    st.markdown("### 🧾 Recent calculations")
    for entry in reversed(st.session_state.history[-8:]):
        st.text(entry)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Built with ❤️ using Streamlit — Casio FX-991 style")
