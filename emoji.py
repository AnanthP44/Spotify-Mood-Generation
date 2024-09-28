import streamlit as st

# Title and subheading with specific colors
st.markdown("""
    <style>
    .title {
        color: white;
        font-size: 2em;
    }
    .subheading {
        color: white;
        font-size: 1.5em;
    }
    .stTextInput input {
        background-color: #1ED760; /* Background color of the input field */
        color: black; /* Text color inside the input field */
        font-weight: bold; /*Make the text bold*/
    }
    </style>
    <h1 class="title">Describe your emotion in one sentence?</h1>
    <p class="subheading">Enter your mood here:</p>
""", unsafe_allow_html=True)

# User input
mood = st.text_input("", key="moodInput1")

#user camera input

