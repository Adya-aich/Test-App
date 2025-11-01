import streamlit as st

# Streamlit app title
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")
st.title("🧮 Simple Calculator")

# User inputs
num1 = st.number_input("Enter first number", format="%.2f")
num2 = st.number_input("Enter second number", format="%.2f")

# Operation selection
operation = st.selectbox("Select operation", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])

# Perform calculation
if st.button("Calculate"):
    if operation == "Addition (+)":
        result = num1 + num2
        st.success(f"The result is: {result}")
    elif operation == "Subtraction (-)":
        result = num1 - num2
        st.success(f"The result is: {result}")
    elif operation == "Multiplication (×)":
        result = num1 * num2
        st.success(f"The result is: {result}")
    elif operation == "Division (÷)":
        if num2 != 0:
            result = num1 / num2
            st.success(f"The result is: {result}")
        else:
            st.error("Error: Division by zero is not allowed.")
