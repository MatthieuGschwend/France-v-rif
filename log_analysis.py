import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title('Log Analysis')

    st.header('Study of errors')

    st.subheader('Raw Data')
    log_data = pd.read_csv("log.csv")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("log.csv"):
            st.dataframe(log_data)
    with col2:
        with st.expander("columns"):
            st.text("Columns explanation:")
            body = """
            * **url**: url of the product page.

            * **error_message**: error message when the function got an
            exception.

            * **function_name**: name of the function.

            * **error_level**: can either be **error**, **warning** or nothing if
            everything went well.

            * **date**: date when the function was called.

            * **process_time**: how long the function took to complete.

            * **replicas_nb_by_url**: number of replicas gathered from google
            shopping by setting the url as the query.

            * **replicas_nb_by_name**: number of replicas gathered from google
            shopping by setting the product name as the query.

            * **replicas_nb_by_image**: number of replicas gathered from google
            image by setting the image url as the query.
            """
            st.markdown(body, unsafe_allow_html=False)

    st.subheader('Error counts')
    error_count_by_function = log_data.groupby(
        ['function_name']).count()[["error_message"]]
    error_count_by_function = error_count_by_function.sort_values(
        by='error_message', ascending=False)

    col1_, col2_ = st.columns(2)
    with col1_:
        with st.expander("Error count by function"):
            st.dataframe(error_count_by_function)

    with col2_:
        with st.expander("Bar chart comparison"):
            error_count_by_function = error_count_by_function[
                error_count_by_function["error_message"]>0]
            bar_fig = px.bar(
                error_count_by_function,
                x=error_count_by_function.index,
                y=["error_message"],
                height=295,
                width=680)
            st.plotly_chart(bar_fig)

    with st.expander("Pie chart comparison"):
        error_count = log_data.groupby(
            ['function_name']).count()[["error_message"]].reset_index()
        error_count = error_count[error_count["error_message"]>0]

        pie_fig = px.pie(
            error_count,
            values='error_message',
            names="function_name",
            title='Error count by function')

        st.plotly_chart(pie_fig)


    log_data["error_message"] = log_data["error_message"].str.split(", url=URL").str[0]
    log_data["error_message"] = log_data["error_message"].str.split("byte").str[0]

    st.subheader('What are the error messages?')
    with st.expander("Errors detail"):
        error_count_by_message = log_data['error_message'].value_counts()
        error_count_by_message = error_count_by_message.rename_axis('error_message')
        error_count_by_message = error_count_by_message.reset_index(name='counts')
        error_count_by_message = error_count_by_message[
            error_count_by_message["counts"]>1]
        st.dataframe(error_count_by_message)

    with st.expander("Pie chart comparison"):
        pie_fig2 = px.pie(
            error_count_by_message,
            values='counts',
            names="error_message",
            title='Error count by message error')
        st.plotly_chart(pie_fig2)

    st.subheader('On what proportion do the error occurs?')
    error_count_by_message["percentage_over_all_urls"] = error_count_by_message["counts"]*100/len(log_data["url"].unique())

    with st.expander("Percentage of occurence"):
        st.dataframe(error_count_by_message[[
        "error_message", "percentage_over_all_urls"]])

    st.subheader('To which function is the error message linked?')
    log_data_grouped = log_data[~log_data["error_message"].str.contains(
        "/shopping/product/", na=False)]
    log_data_grouped = log_data_grouped.groupby([
        'function_name', 'error_message', 'error_level']).count()[["url"]]
    with st.expander("Function with its error message"):
        st.dataframe(log_data_grouped)

    st.subheader('To which urls are the diffbot error messages linked?')
    problematic_urls = log_data["url"][log_data["error_message"].str.contains("objects", na=False)]
    with st.expander("Problematic urls"):
        st.write("len:", len(problematic_urls))
        for url in problematic_urls:
            st.write(url)

    st.header('Study of processing time of functions')
    