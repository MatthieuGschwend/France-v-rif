import interface_fr
import interface_en
import log_analysis_en
import log_analysis_fr
import streamlit as st


st.set_page_config(layout="wide")
PAGES = {
    "FR":
    {
        "Analyse des processus de collecte de données": log_analysis_fr,
        "Analyse des données": interface_fr
    },
    "EN":
    {
        "Analysis of data collection processes": log_analysis_en,
        "Data analysis": interface_en
    }
}

st.sidebar.image("logo.png", width=100)

st.sidebar.title("Lang 🌍")
lang_option = st.sidebar.selectbox("", ("FR", "EN"))
if lang_option == "FR":
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Onglets", list(PAGES["FR"].keys()))
    page = PAGES["FR"][selection]
    page.app()
else:
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Onglets", list(PAGES["EN"].keys()))
    page = PAGES["EN"][selection]
    page.app()
