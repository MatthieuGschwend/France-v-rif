import streamlit as st
import asyncio
from legal_notice import main_legal_notice


def app():
    domain_name = st.text_input("Domain name")
    if domain_name:
        res = asyncio.run(main_legal_notice(domain_name))
        st.write(res)