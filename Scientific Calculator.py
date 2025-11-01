import streamlit as st
import math

st.set_page_config(page_title="Casio fx-991 | Scientific Calculator", page_icon="🧮")

st.title("🧮 Casio fx-991 - Scientific Calculator")
st.markdown("A simple yet powerful scientific calculator built with Streamlit.")

# --- Input section ---
expression = st.text_input("Enter your expression:", placeholder="e.g. sin(30) + log(10) * sqrt(16)")

# --- Helper functions ---
def evaluate_expression(expr):
    try:
        # Replace common math notations
        expr = expr.replace("^", "**")
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))
        
        # Allowed functions
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names["abs"] = abs
        
        # Evaluate safely
        result = eval(expr, {"__builtins__": None}, allowed_names)
        return result
    except Exception as e:
        return f"❌ Error: {e}"

# --- Buttons and Layout ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("sin()"):
        st.session_state["expression"] = st.session_state.get("expression", "") + "sin("
with col2:
    if st.button("cos()"):
        st.session_state["expression"] = st.session_state.get("expression", "") + "cos("
with col3:
    if st.button("tan()"):
        st.session_state["expression"] = st.session_state.get("expression", "") + "tan("

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("log()"):
        st.session_state["expression"] = st.session_state.get("expression", "") + "log("
with col5:
    if st.button("sqrt()"):
        st.session_state["expression"] = st.session_state.get("expression", "") + "sqrt("
with col6:
    if st.button("π"):
        st.session_state["expression"] = st.session_state.get("expression", "") + "π"

# --- Evaluate ---
if expression:
    result = evaluate_expression(expression)
    st.subheader(f"Result: {result}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Inspired by Casio fx-991 series")
