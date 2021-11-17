import interface
import log_analysis
import streamlit as st


st.set_page_config(layout="wide")
PAGES = {
    "Log analysis": log_analysis,
    "Analyse des données": interface
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Onglets", list(PAGES.keys()))
page = PAGES[selection]
page.app()
