import streamlit as st
import streamlit.components.v1 as components
import webbrowser



def app():
    link = '[Debugger](http://161.35.202.8:8050/)'
    st.markdown(link, unsafe_allow_html=True)