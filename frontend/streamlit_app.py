import streamlit as st
import requests

st.title(
    "AI Fridge Chef"
)

image = st.file_uploader(
    "Upload fridge photo"
)

preference = st.text_input(
    "What do you want?"
)

if st.button("Generate recipe"):

    response = requests.post(
        "http://localhost:8000/recipe",
        files={
            "image": image
        },
        data={
            "preference": preference
        }
    )

    st.write("Status:", response.status_code)

    try:
        st.json(response.json())
    except Exception:
        st.text(response.text)