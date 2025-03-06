import streamlit as st
import random
import pyperclip

# Set page configuration
st.set_page_config(page_title="Password Generator", page_icon="🔒", layout="centered")

# Password strength bar function
def get_strength_color(password):
    length = len(password)
    if length <= 6:
        return 'red', length  # Weak
    elif 7 <= length <= 12:
        return 'yellow', length  # Medium
    else:
        return 'green', length  # Strong

# Generate password function
def generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols):
    uppercase_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase_chars = "abcdefghijklmnopqrstuvwxyz"
    number_chars = "0123456789"
    symbol_chars = "!@#$%^&*()_+[]{}|;:,.<>?"

    all_chars = ""
    if include_uppercase:
        all_chars += uppercase_chars
    if include_lowercase:
        all_chars += lowercase_chars
    if include_numbers:
        all_chars += number_chars
    if include_symbols:
        all_chars += symbol_chars

    if not all_chars:
        return "Please select at least one character type."

    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

# UI layout
st.markdown("<h2 style='text-align: center; color: #FF6347;'>🔒 Password Generator</h2>", unsafe_allow_html=True)

length = st.slider("Select Password Length", min_value=6, max_value=18, value=12, step=1)
include_uppercase = st.checkbox("Include Uppercase Letters", value=True)
include_lowercase = st.checkbox("Include Lowercase Letters", value=True)
include_numbers = st.checkbox("Include Numbers", value=True)
include_symbols = st.checkbox("Include Symbols", value=True)

if st.button("Generate Password"):
    password = generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
    st.text_input("Generated Password", value=password, key="password_box")

    # Password strength checker
    if password != "Please select at least one character type.":
        color, length = get_strength_color(password)
        total_bars = 18
        filled_bars = min(length, total_bars)  # Ensure filled_bars does not exceed total_bars
        empty_bars = total_bars - filled_bars

        # Display colored bars
        bar_html = (
            "<div style='display: flex;'>"
            + "".join([f"<div style='width: 10px; height: 20px; background-color: {color}; margin-right: 2px;'></div>" for _ in range(filled_bars)])
            + "".join(["<div style='width: 10px; height: 20px; background-color: #e0e0e0; margin-right: 2px;'></div>" for _ in range(empty_bars)])
            + "</div>"
        )
        st.markdown(bar_html, unsafe_allow_html=True)

        # Password strength message
        if color == 'red':
            st.warning("Weak Password! Consider increasing the length.")
        elif color == 'yellow':
            st.info("Moderate Password! Could be stronger.")
        else:
            st.success("Strong Password!")

    # Copy to clipboard button
    if st.button("Copy to Clipboard"):
        pyperclip.copy(password)
        st.success("Password copied to clipboard!")

st.markdown("<p style='text-align: center; color: #808080;'>Developed by Azmat Ali</p>", unsafe_allow_html=True)
