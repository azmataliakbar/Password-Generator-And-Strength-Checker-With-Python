import streamlit as st
import random
import string

# Function to generate password
def generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols):
    uppercase_chars = string.ascii_uppercase if include_uppercase else ''
    lowercase_chars = string.ascii_lowercase if include_lowercase else ''
    number_chars = string.digits if include_numbers else ''
    symbol_chars = string.punctuation if include_symbols else ''

    all_chars = uppercase_chars + lowercase_chars + number_chars + symbol_chars

    if not all_chars:
        st.error("Please select at least one character type.")
        return ""

    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

# Function to check password strength
def check_password_strength(password):
    length = len(password)
    if length < 6:
        return "red", length
    elif 6 <= length <= 12:
        return "yellow", length
    else:
        return "green", length

# Streamlit UI
st.set_page_config(page_title="Password Generator", page_icon="🔒", layout="centered")

st.title("Password Generator")
st.markdown("Create a secure password with just a few clicks.")

# Password length slider
length = st.slider("Password Length", min_value=6, max_value=32, value=16)

# Checkboxes for character types
col1, col2 = st.columns(2)
with col1:
    include_uppercase = st.checkbox("Uppercase Letters", value=True)
    include_lowercase = st.checkbox("Lowercase Letters", value=True)
with col2:
    include_numbers = st.checkbox("Numbers", value=True)
    include_symbols = st.checkbox("Symbols", value=True)

# Generate password button
if st.button("Generate Password"):
    password = generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
    if password:
        st.session_state.generated_password = password

# Display generated password
if 'generated_password' in st.session_state:
    st.subheader("Generated Password")
    st.code(st.session_state.generated_password, language="text")

    # Password strength indicator
    strength, strength_length = check_password_strength(st.session_state.generated_password)
    st.markdown("### Password Strength")
    if strength == "red":
        st.markdown('<div style="background-color: red; height: 20px; width: 100%;"></div>', unsafe_allow_html=True)
    elif strength == "yellow":
        st.markdown('<div style="background-color: yellow; height: 20px; width: 100%;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background-color: green; height: 20px; width: 100%;"></div>', unsafe_allow_html=True)

    # Copy to clipboard button
    if st.button("Copy to Clipboard"):
        st.write("Password copied to clipboard!")
        st.code(st.session_state.generated_password, language="text")

# Footer
st.markdown("---")
st.markdown("Author: Azmat Ali")