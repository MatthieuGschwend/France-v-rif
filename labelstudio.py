import streamlit as st
import streamlit.components.v1 as components
import requests


def post_to_label_studio_app(text):
    requests.post(
        "http://161.35.202.8:8080/api/projects/1/import",
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token 2860c48100a92de0c80ccca21751a17e1a79ec08"
        },
        json=[{"text": text}]
    )


def app():
    form = st.form(key='label form')
    text_input = form.text_area(label='Enter a text to label. This will be sent to the label studio app.')
    submit_button = form.form_submit_button(label='Submit')
    if submit_button:
        try:
            post_to_label_studio_app(text_input)
        except Exception as e:
            st.error(e)
        st.success('Successfully sent to the label sutdio app!')