import interface_fr
import log_analysis_en
import log_analysis_fr
import streamlit as st


st.set_page_config(layout="wide")
PAGES = {
    "FR":
    {
        "Log analysis": log_analysis_fr,
        "Analyse des données": interface_fr
    },
    "EN":
    {
        "Log analysis": log_analysis_en,
        "Analyse des données": interface_fr
    }
}

st.sidebar.title("Lang 🌍")
lang_option = st.sidebar.selectbox("Onglets", ("FR", "EN"))
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
