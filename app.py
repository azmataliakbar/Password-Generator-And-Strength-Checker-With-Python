import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from io import BytesIO
import plotly.express as px
import requests
import json
from datetime import datetime
import time
import random
import string

# Set page config - this must be the first Streamlit command
st.set_page_config(
    page_title="Password Generator",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container */
    .main-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 10px;
    }
    
    /* App title */
    .app-title {
        color: #f705f7; /* rose-700 equivalent */
        text-align: center;
        font-size: 36px;
        margin-bottom: 5px;
        font-weight: bold;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* App subtitle */
    .app-subtitle {
        color: green;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* Password display */
    .password-display {
        font-size: 40px;
        font-weight: bold;
        color: #b91c1c; /* red-700 equivalent */
        text-align: center;
        margin: 15px 0;
        padding: 10px;
        background-color: #fef3c7; /* yellow-100 equivalent */
        border-radius: 8px;
        border: 1px solid #fcd34d; /* yellow-300 equivalent */
    }
    
    /* Labels */
    .label {
        font-weight: bold;
        margin-bottom: 5px;
        font-size: 25px;
        color: red;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #2563eb; /* blue-600 equivalent */
        font-size: 20px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    /* Override Streamlit's default styling */
    .stButton > button {
        background-color: #4f46e5 !important; /* indigo-600 equivalent */
        color: white !important;
        font-weight: bold !important;
        font-size: 40px !important;
        width: 100% !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #4338ca !important; /* indigo-700 equivalent */
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        margin-bottom: 10px;
    }
    
    /* Slider styling */
    .stSlider {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    /* Strength meter container */
    .strength-meter {
        display: flex;
        margin: 15px 0;
        gap: 3px;
    }
    
    /* Strength bar */
    .strength-bar {
        height: 60px;
        flex-grow: 1;
        border-radius: 4px;
        background-color: #e5e7eb; /* gray-200 equivalent */
    }
    
    /* Red strength */
    .strength-red {
        background-color: #ef4444; /* red-500 equivalent */
    }
    
    /* Yellow strength */
    .strength-yellow {
        background-color: #f59e0b; /* amber-500 equivalent */
    }
    
    /* Green strength */
    .strength-green {
        background-color: #10b981; /* emerald-500 equivalent */
    }
    
    /* Page background */
    .main {
        background: linear-gradient(135deg, #ec4899, #8b5cf6) !important;
        background-attachment: fixed !important;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .app-title {
        font-size: 36px;
        }
        
        .app-subtitle {
        font-size: 16px;
        margin-top: 30px;
        margin-bottom: 10px;
        color: green;
        }
        
        .password-display {
            font-size: 16px;
        }
    }
    
    /* Success message */
    .success-message {
        color: #059669; /* emerald-600 equivalent */
        font-weight: bold;
        text-align: center;
        padding: 8px;
        border-radius: 4px;
        background-color: #d1fae5; /* emerald-100 equivalent */
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'password' not in st.session_state:
    st.session_state.password = ""
if 'password_length' not in st.session_state:
    st.session_state.password_length = 16
if 'converted_amount' not in st.session_state:
    st.session_state.converted_amount = "0.00"
if 'exchange_rates' not in st.session_state:
    st.session_state.exchange_rates = {}
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = None
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

# Function to generate password
def generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols):
    chars = ""
    if include_uppercase:
        chars += string.ascii_uppercase
    if include_lowercase:
        chars += string.ascii_lowercase
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += string.punctuation
    
    if not chars:
        st.error("Please select at least one character type.")
        return ""
    
    return ''.join(random.choice(chars) for _ in range(length))

# Function to render strength meter
def render_strength_meter(password_length):
    # Define constants to avoid duplication
    EMPTY_BAR = '<div class="strength-bar"></div>'
    RED_BAR = '<div class="strength-bar strength-red"></div>'
    YELLOW_BAR = '<div class="strength-bar strength-yellow"></div>'
    GREEN_BAR = '<div class="strength-bar strength-green"></div>'
    
    # Calculate how many bars to fill for each color
    red_bars = min(password_length, 6)
    yellow_bars = max(0, min(password_length - 6, 6))
    green_bars = max(0, min(password_length - 12, 6))
    
    # Create HTML for the strength meter
    strength_meter_html = '<div class="strength-meter">'
    
    # Add red bars
    for i in range(6):
        if i < red_bars:
            strength_meter_html += RED_BAR
        else:
            strength_meter_html += EMPTY_BAR
    
    # Add yellow bars
    for i in range(6):
        if i < yellow_bars:
            strength_meter_html += YELLOW_BAR
        else:
            strength_meter_html += EMPTY_BAR
    
    # Add green bars
    for i in range(6):
        if i < green_bars:
            strength_meter_html += GREEN_BAR
        else:
            strength_meter_html += EMPTY_BAR
    
    strength_meter_html += '</div>'
    
    # Add strength text
    if password_length <= 6:
        strength_text = '<div style="text-align: center; color: #ef4444; font-weight: bold;">Weak Password</div>'
    elif password_length <= 12:
        strength_text = '<div style="text-align: center; color: #f59e0b; font-weight: bold;">Medium Password</div>'
    else:
        strength_text = '<div style="text-align: center; color: #10b981; font-weight: bold;">Strong Password</div>'
    
    return strength_meter_html + strength_text

# Main app container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# App title
st.markdown('<div class="app-title">Password Generator & Strength Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Create a secure password with just a few clicks.</div>', unsafe_allow_html=True)

# Password length slider
st.markdown('<div class="label">Password Length</div>', unsafe_allow_html=True)
# Fixed: Added proper label instead of empty string
password_length = st.slider("Password Length", min_value=4, max_value=32, value=st.session_state.password_length, step=1, label_visibility="visible")
st.session_state.password_length = password_length

# Character type options
st.markdown('<div class="label">Include:</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    include_uppercase = st.checkbox("Uppercase Letters", value=True)
    include_numbers = st.checkbox("Numbers", value=True)

with col2:
    include_lowercase = st.checkbox("Lowercase Letters", value=True)
    include_symbols = st.checkbox("Symbols", value=True)

# Generate password button
if st.button("Generate Password"):
    st.session_state.password = generate_password(
        password_length,
        include_uppercase,
        include_lowercase,
        include_numbers,
        include_symbols
    )

# Display password
st.markdown('<div class="label">Generated Password</div>', unsafe_allow_html=True)
if st.session_state.password:
    st.markdown(f'<div class="password-display">{st.session_state.password}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="password-display">Your password will appear here</div>', unsafe_allow_html=True)

# Password strength meter
if st.session_state.password:
    st.markdown('<div class="label">Password Strength</div>', unsafe_allow_html=True)
    st.markdown(render_strength_meter(len(st.session_state.password)), unsafe_allow_html=True)

# Copy to clipboard button (using Streamlit's built-in functionality)
if st.session_state.password:
    st.code(st.session_state.password, language=None)
    st.success("👆 Copy the password to your clipboard!")

# Author footer
st.markdown('<div class="footer">Author: Azmat Ali</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container