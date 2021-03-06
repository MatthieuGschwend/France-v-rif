import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


colors = ['#2BCDC1', '#393E46', '#F7CC57', '#F66095']
log_data = pd.read_csv("log.csv")


def app():

    st.title('Analysis of data collection processes')

    st.header('Study of errors :microscope:')

    # Filter to keep only the errors and not the warnings
    error_data = log_data[log_data["error_level"].isin(["error"])]
    st.header('Synthesis')
    synt_col1, synt_col2 = st.columns(2)
    with synt_col1:
        st.subheader('Success/Fail rate')
        # Cleaning to regroup the same message errors written diffrently
        error_data["error_message"] = error_data["error_message"].str.split(", url=URL").str[0]
        error_data["error_message"] = error_data["error_message"].str.split("byte").str[0]

        # Count of each error occurence
        error_count_by_message = error_data['error_message'].value_counts()
        error_count_by_message = error_count_by_message.rename_axis('error_message')
        error_count_by_message = error_count_by_message.reset_index(name='counts')
        error_count_by_message = error_count_by_message[
            error_count_by_message["counts"]>0]

        # Percentage of occurence of each error
        error_count_by_message["percentage_over_all_urls"] = error_count_by_message["counts"] \
            *100/len(log_data["url"].unique())
        
        fail_rate = error_count_by_message["percentage_over_all_urls"].sum()
        success_rate = 100 - fail_rate
        labels = ['Succès','Échec']
        values = [success_rate, fail_rate]

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_traces(marker=dict(
            colors=colors))
        st.plotly_chart(fig, use_container_width=True)

    with synt_col2:
        st.subheader("Time (in second) distribution of the main function")
        main_function_data = log_data[log_data["function_name"].isin(
            ["get_product_vs_replicas"])]

        hist_data = main_function_data["process_time"].to_list()
        group_labels = "get_product_vs_replicas"
        fig1 = ff.create_distplot([hist_data], [group_labels], bin_size=2, colors=colors)
        fig1.update_xaxes(range=[0, 200])
        st.plotly_chart(fig1, use_container_width=True)

    st.subheader('Raw Data')

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

            * **process_time**: how long the function took to complete. In second.

            * **replicas_nb_by_url**: number of replicas gathered from google
            shopping by setting the url as the query.

            * **replicas_nb_by_name**: number of replicas gathered from google
            shopping by setting the product name as the query.

            * **replicas_nb_by_image**: number of replicas gathered from google
            image by setting the image url as the query.
            """
            st.markdown(body, unsafe_allow_html=False)

    st.header('Error counts')

    error_count_by_function = error_data.groupby(
        ['function_name']).count()[["error_message"]]
    error_count_by_function = error_count_by_function.sort_values(
        by='error_message', ascending=False)

    col1_, col2_ = st.columns(2)
    with col1_:
        # st.subheader("Error count by function")
        # st.dataframe(error_count_by_function)
        st.subheader("Error count by function")
        error_count = error_data.groupby(
            ['function_name']).count()[["error_message"]].reset_index()
        error_count = error_count[error_count["error_message"]>0]

        pie_fig = px.pie(
            error_count,
            values='error_message',
            names="function_name")

        st.plotly_chart(pie_fig, use_container_width=True)
    with col2_:
        st.subheader("Bar chart comparison")
        error_count_by_function = error_count_by_function[
            error_count_by_function["error_message"]>0]
        bar_fig = px.bar(
            error_count_by_function,
            x=error_count_by_function.index,
            y=["error_message"])
        st.plotly_chart(bar_fig, use_container_width=True)

    st.header("What are the error messages?")
    err_mssg_col1, err_mssg_col2 = st.columns(2)
    with err_mssg_col1:
        log_data_grouped = error_data[~error_data["error_message"].str.contains(
            "/shopping/product/", na=False)]

        log_data_grouped = log_data_grouped.groupby([
            'function_name', 'error_message', 'error_level']).count()[["url"]]
        log_data_grouped["percentage_over_all_urls"] = log_data_grouped["url"] \
                *100/len(log_data["url"].unique())
        log_data_grouped = log_data_grouped[log_data_grouped["url"]>1]
        log_data_grouped = log_data_grouped.sort_values(by="url", ascending=False)
        st.subheader("Function with its error message")
        st.dataframe(log_data_grouped)

    with err_mssg_col2:
        st.subheader("Error rate per error message")
        data_to_plot = error_count_by_message[error_count_by_message["counts"]>1]
        pie_fig2 = px.pie(
            data_to_plot,
            values='counts',
            names="error_message")
        st.plotly_chart(pie_fig2, use_container_width=True)

    st.subheader("Try the product page scraping functions")

    query = st.text_input("Url de la page produit")
    function_test_col1, function_test_col2 = st.columns(2)
    with function_test_col1:
        st.subheader("Diffbot")
        key_diffbot = "9a98f884113fbc6864d6b5c56276d4d8"
        if query:
            with st.spinner('Wait for it...'):
                start_time = time.time()
                params = {'token':key_diffbot, 'url':query, 'timeout':30000}
                endpoint = "https://api.diffbot.com/v3/product"
                res = requests.get(endpoint, params=params)
                end_time = time.time()
                exec_time = end_time - start_time
                exec_time = round(exec_time, 2)
                st.write(f"Execution time :", exec_time, " seconds")
                st.write(res.json())

    with function_test_col2:
        st.subheader("Homemade scraper")

    problematic_urls = log_data["url"][log_data["error_message"].str.contains(
        "objects", na=False)]
    with st.expander("Urls problématiques"):
        st.write("total urls:", len(log_data))
        st.write("total problematic_urls:", len(problematic_urls))
        for url in problematic_urls:
            st.write(url)

    st.header('Study of processing time of functions :hourglass:')
    with st.expander("Expand"):
        st.subheader('Global time taken')

        st.subheader('Diffbot vs Old scraper')

        st.subheader("Time (in second) distribution of the diffbot function and old scraper function")

        diffbot_data = log_data["process_time"][log_data["function_name"].isin(
            ["data_Diffbot"])].to_list()
        old_scraper_data = log_data["process_time"][log_data["function_name"].isin(
            ["get_data"])].to_list()

        hist_data_1 = [diffbot_data, old_scraper_data]
        group_labels_1 = ["data_Diffbot", "get_data"]
        fig2 = ff.create_distplot(hist_data_1, group_labels_1, colors=colors)
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader('Old scraper detail processing time')

        st.subheader("Time (in second) distribution of each function that compose old scraper function")
            
        old_sc_func_1 = log_data["process_time"][log_data["function_name"].isin(
            ["get_name"])].to_list()
        old_sc_func_2 = log_data["process_time"][log_data["function_name"].isin(
            ["get_description"])].to_list()
        old_sc_func_3 = log_data["process_time"][log_data["function_name"].isin(
            ["get_price"])].to_list()
        old_sc_func_4 = log_data["process_time"][log_data["function_name"].isin(
            ["get_image"])].to_list()

        hist_data_2 = [old_sc_func_1, old_sc_func_2, old_sc_func_3, old_sc_func_4]
        group_labels_2 = ["get_name", "get_description", "get_price", "get_image"]
        fig3 = ff.create_distplot(hist_data_2, group_labels_2, bin_size=0.05, colors=colors)
        fig3.update_xaxes(range=[0, 4])
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader('Aliexpress vs Google')

        st.subheader("Time (in second) distribution of the replicas collector functions")
            
        func_1 = log_data["process_time"][log_data["function_name"].isin(
            ["data_Aliexpress"])].to_list()
        func_2 = log_data["process_time"][log_data["function_name"].isin(
            ["data_Google_combined"])].to_list()

        hist_data_3 = [func_1, func_2]
        group_labels_3 = ["data_Aliexpress", "data_Google_combined"]
        fig4 = ff.create_distplot(hist_data_3, group_labels_3, bin_size=0.1, colors=colors)
        st.plotly_chart(fig4, use_container_width=True)

        st.subheader('Google Vision')
        
        st.subheader("Time (in second) distribution of the google image classification function")
            
        goo_func_1 = log_data["process_time"][log_data["function_name"].isin(
            ["dataset_Google_Vision"])].to_list()
        goo_func_2 = log_data["process_time"][log_data["function_name"].isin(
            ["data_Google_Vision"])].to_list()

        hist_data_4 = [goo_func_1, goo_func_2]
        group_labels_4 = ["dataset_Google_Vision", "data_Google_Vision"]

        fig5 = ff.create_distplot(hist_data_4, group_labels_4, bin_size=0.1, colors=colors)
        fig5.update_xaxes(range=[0, 10])
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("""
        * **dataset_Google_Vision**: when the google image
        classification function is called asynchronously when there are
        multiple images. Called for replicas image categories.
        
        * **data_Google_Vision**: when the google image
        classification function is called only for one image. Called for the
        product page image classification.
        """)
