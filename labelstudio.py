import streamlit as st
import streamlit.components.v1 as components
import webbrowser


def app():
    url = "http://161.35.202.8:8080"
    if st.button('Open label studio'):
        webbrowser.open_new_tab(url)
