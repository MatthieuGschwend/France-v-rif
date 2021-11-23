import streamlit as st
st.set_page_config(layout="wide")
import interface_fr
import log_analysis_en
import log_analysis_fr
import legal_notice_fr
import legal_notice_en


PAGES = {
    "FR":
    {
        "Analyse des processus de collecte de données": log_analysis_fr,
        "Analyse des données": interface_fr,
        "Test de l'algo de mentions légales": legal_notice_fr
    },
    "EN":
    {
        "Analysis of data collection processes": log_analysis_en,
        "Analyse des données": interface_fr,
        "Test of legal notice algo": legal_notice_en
    }
}

st.sidebar.image("image/logo.png", width=100)

st.sidebar.title("Lang 🌍")
lang_option = st.sidebar.selectbox("", ("FR", "EN"))
if lang_option == "FR":
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("", list(PAGES["FR"].keys()))
    page = PAGES["FR"][selection]
    page.app()
else:
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("", list(PAGES["EN"].keys()))
    page = PAGES["EN"][selection]
    page.app()