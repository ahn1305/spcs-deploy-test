import streamlit as st
import requests

st.title("SPCS + Snowflake Streamlit Demo")

name = st.text_input("Enter your name")

if st.button("Send to Backend"):
    if name:
        try:
            url = "https://<your-spcs-service-url>/process"
            response = requests.get(url, params={"name": name})
            data = response.json()

            st.success(data["message"])

        except Exception as e:
            st.error(f"Error: {e}")
