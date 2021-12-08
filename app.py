import streamlit as st
st.set_page_config(layout="wide")
import interface_fr
import interface_en
import log_analysis_en
import log_analysis_fr
import legal_notice_fr
import legal_notice_en
import debugger
import labelstudio
import yml_extraction


PAGES = {
    "FR":
    {
        "Debugger": debugger,
        "Label Studio": labelstudio,
        "yml extraction test": yml_extraction,
        "Test de l'algo de mentions légales": legal_notice_fr,
        "Analyse des processus de collecte de données": log_analysis_fr,
        "Analyse des données": interface_fr
    },
    "EN":
    {
        "Debugger": debugger,
        "Label Studio": labelstudio,
        "yml extraction test": yml_extraction,
        "Test of legal notice algo": legal_notice_en,
        "Analysis of data collection processes": log_analysis_en,
        "Data analysis": interface_en
    }
}

st.sidebar.image("logo.png", width=100)

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