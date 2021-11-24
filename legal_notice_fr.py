import streamlit as st
import time
import asyncio
from legal_notice import main_legal_notice


def app():
    domain_name = st.text_input("Nom de domaine")
    if domain_name:
        start = time.perf_counter()
        res = asyncio.run(main_legal_notice(domain_name))
        finish = time.perf_counter()
        st.write('Done in ', round(finish-start, 2), ' seconds')
        st.write(res)