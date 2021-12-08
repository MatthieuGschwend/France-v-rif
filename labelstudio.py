import streamlit as st
import streamlit.components.v1 as components
import webbrowser


def app():
    link = '[label studio](http://161.35.202.8:8080/)'
    st.markdown(link, unsafe_allow_html=True)