import streamlit as st
import random
import string

# Initialize session state for password history
if "password_history" not in st.session_state:
    st.session_state.password_history = []

def generate_password(length, min_uppercase, min_digits, min_special):
    # Ensure required characters are included
    password = []
    
    # Add  uppercase letters
    password.extend(random.choices(string.ascii_uppercase, k=min_uppercase))
    
    # Add  digits
    password.extend(random.choices(string.digits, k=min_digits))
    
    # Add  special characters
    password.extend(random.choices(string.punctuation, k=min_special))
    
    # Fill the random characters
    remaining_length = length - len(password)
    if remaining_length > 0:
        all_characters = string.ascii_letters + string.digits + string.punctuation
        password.extend(random.choices(all_characters, k=remaining_length))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

def check_password_strength(password):
    if len(password) < 8:
        return "Weak", 0.25
    elif len(password) < 12:
        return "Medium", 0.5
    elif len(password) < 16:
        return "Strong", 0.75
    else:
        return "Very Strong", 1.0

st.title("🔑 Password Generator & Strength Meter")

# User Inputs
length = st.slider("Select Password Length", 5, 35, 10)
min_uppercase = st.number_input("Minimum Uppercase Letters", 0, length, 1)
min_digits = st.number_input("Minimum Digits", 0, length, 1)
min_special = st.number_input("Minimum Special Characters", 0, length, 1)

# Generate Password Button
if st.button("Generate Password"):
    password = generate_password(length, min_uppercase, min_digits, min_special)
    st.write(f"**Generated Password:** `{password}`")
    
    # Store password in history (keep last 5)
    st.session_state.password_history.insert(0, password)
    st.session_state.password_history = st.session_state.password_history[:5]

    # Check Strength
    strength, score = check_password_strength(password)
    st.write(f"**Password Strength:** {strength}")
    st.progress(score)

# Display Password History
if st.session_state.password_history:
    st.write("🔄 **Last 5 Passwords:**")
    for i, past_password in enumerate(st.session_state.password_history, start=1):
        st.write(f"{i}. `{past_password}`")
