from datetime import timedelta
from pathlib import Path
from time import sleep

import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st


def app():
    #%% 
    @st.cache
    def load_data():
        '''Lecture du fichier csv'''
        data_path = 'collected_data_4.csv'
        data = pd.read_csv(data_path)
        return data


    def mois_annees(nb_mois):
        nb_annes = int(nb_mois/12.)
        nb_mois_ = int(nb_mois) % 12
        an = 'year '
        if nb_annes > 1:
            an = ' years'
        if nb_mois_ == 0:
            return str(nb_annes) + an
        else:
            return str(nb_annes) + an + ' and ' + str(nb_mois_) + ' month'
        

    def boolean_string(oui_ou_non):
        if(oui_ou_non == 1):
            return 'Yes'
        else : 
            return 'No'
        
    #%% Analyse ANOVA globale
    @st.cache
    def classe_anova_replica(data):

        ''' Pour tous les produits nous voulons faires des analyses de
        corrélation entre le label final (product class) avec les propriétés des 
        réplicas : prix des réplicas, proportion de sites Green, proportion de 
        site shopify'''

        liste_item = data['product name'].unique() # liste des produits
        green_moyen = [0]*len(liste_item)
        shopify_moyen = [0]*len(liste_item)
        label_item = [0]*len(liste_item)
        age_article = [0]*len(liste_item)
        article_prix = [0]*len(liste_item)
        #Recuperation des information par produit
        i = 0
        for nom_produit in liste_item:
            data_item = data[data['product name'] == nom_produit]
            green_moyen[i] = data_item['replica is_green_website'].mean()
            shopify_moyen[i] = data_item['replica is_shopify'].mean()
            label_item[i] = data_item['product class'].values[0]
            age_article[i] = data_item['product website_age_in_months'].values[0]
            article_prix[i] = data_item['product price'].values[0]
            i += 1            
        # Construction d'un data frame avec toutes les infos 
        df = pd.DataFrame({'Product name':liste_item,
                           'Proportion Green Web Site replicas': green_moyen, 
                           'Proportion Shopify replicas': shopify_moyen,
                           'Product class' : label_item,
                           'Age' : age_article,
                           'Product price': article_prix
                           })
        return df


    def vue_ensemble_data(data_classe, prix_min, prix_max):
        data_ = data_classe[data_classe['Product price'] > prix_min]
        data_ = data_[data_['Product price'] < prix_max]
        fig = px.scatter(data_, x='Product price', y='Age',
                         color='Product class',
                         marginal_y="box", marginal_x="box", 
                         trendline="ols", template="simple_white",
                         color_discrete_sequence=['grey','green','orange'])
        return st.plotly_chart(fig, use_container_width=True)


    def calcul_correlation_anova(data_classe, var_qualitative):
        ''' Raport de corrélation entre une variable qualitative x et quantitative y'''
        moyenne = data_classe[var_qualitative].mean()
        classes = []
        for classe in data_classe['Classe du produit'].unique():
            val_classe = data_classe[data_classe['Classe du produit'] == classe][var_qualitative]
            classes.append({'ni': len(val_classe),
                            'moyenne_classe': val_classe.mean()})
        SCT = sum([(yj-moyenne)**2 for yj in data_classe[var_qualitative]])
        SCE = sum([c['ni']*(c['moyenne_classe']-moyenne)**2 for c in classes])
        correlation_lien = "[correlation]" + '(https://en.wikipedia.org/wiki/Correlation_ratio )'
        return st.write('Le rapport de '+correlation_lien+' entre la ' + str(var_qualitative)
                        +' et les classes des produits est de : ' + 
                        str(round(SCE/SCT,4)))

    #%% TEST
    def interface():  

        #st.title('Visualisation du data frame')
        data = load_data()
        
        if st.sidebar.checkbox("Collected data", value=True):

            #mode = st.sidebar.selectbox('Liste des items',np.insert(liste_items,0," "))
            st.title("Collected data")
            #st.write(data_item)
            #st.subheader(str(mode))
            col1, col2 = st.columns(2)
            with col1:
                st.header('Initial product')
                liste_items = data['product name'].unique()
                mode = st.selectbox('Product list', liste_items)
                data_item = data[data['product name'] == mode]
                image_produit = data_item['product image'].values[0]
                st.image(image_produit, width = 200)

            with col2:
                st.header('Replicas')
                liste_replicas = data_item['replica name'].unique()
                replica = st.selectbox('Replica list', liste_replicas)
                data_item_replica = data_item[data_item['replica name']==replica]
                image_replica = data_item_replica['replica image'].values[0]
                st.image(image_replica, width = 200)
                
            
            col3, col4 = st.columns(2)
            with col3:
                # on recolte les informations sur le produit et on affiche
                product_url  = data_item['product url'].values[0]
                product_url = "[Product link]" + '(' + product_url + ')'
                product_description = data_item['product description'].values[0]
                product_prix = str(data_item['product price'].values[0])
                product_web_site  = data_item['product domain'].values[0]
                product_web_site = "["+product_web_site +"]" + '(https://' \
                    + product_web_site + ')'
                product_green = data_item['product is_green_website'].values[0]
                product_age_months = data_item['product website_age_in_months'].values[0]
                product_shopify = data_item['product is_shopify'].values[0]
                product_class = data_item['product class'].values[0]
                
                st.markdown(product_url)
                st.text_area('Description',value = product_description, height = 180)
                st.markdown('- Price : ' + product_prix +' euros' )
                st.markdown('- Web site : ' + product_web_site)
                st.markdown('- Green web site : ' + boolean_string(product_green))
                st.markdown('- Age : ' + mois_annees(product_age_months))
                st.markdown('- Shopify : ' + boolean_string(product_shopify))
                st.markdown('- Product class : ' + product_class)
                


            with col4:
                # on recolte les informations sur la réplica et on affiche
                replica_url = data_item_replica['replica url'].values[0]
                replica_url = "[Replica link]" + '(' + replica_url + ')'
                replica_description = data_item_replica['replica description'].values[0]
                replica_prix = str(data_item_replica['replica price'].values[0])
                replica_web_site  = data_item_replica['replica domain'].values[0]
                replica_web_site = "["+replica_web_site +"]" + '(https://' \
                    + replica_web_site + ')'
                replica_green = data_item_replica['replica is_green_website'].values[0]
                replica_age_months = data_item_replica['replica website_age_in_months'].values[0]
                replica_shopify = data_item_replica['replica is_shopify'].values[0]
                
                st.markdown(replica_url)
                st.text_area('Description',value = replica_description, height = 180)
                st.markdown('- Price : ' + replica_prix +' euros' )
                st.markdown('- Web site : ' + replica_web_site)
                st.markdown('- Green web site : ' + boolean_string(replica_green))
                st.markdown('- Age : ' + mois_annees(replica_age_months))
                st.markdown('- Shopify : ' + boolean_string(replica_shopify))
                



            st.header("Information on all replicas")
            col5, col6 = st.columns([1, 2])
            with col5:
                st.markdown('-  Number of replicas : ' +  str(round(data_item.shape[0],2)))
                st.markdown('- Average price : ' +  str(round(data_item['replica price'].mean(),2)) )
                st.markdown('- Green site web (%) : '  + 
                        str(round(data_item['replica is_green_website'].mean() * 100,2)))
                st.markdown('- Average afluence : ' +  str(round(data_item['rank'].mean(),2)))

            with col6:
                genre = st.radio("Additional visualization",('Domains', 
                                                                 'Affluence/Price/Age', 'Images'))
            if genre == 'Domains':
                nb_domaine_replica = data_item["replica domain"].value_counts().reset_index()            
                #camembert(nb_domaine_replica,'index','replica domain')
                fig = px.pie(nb_domaine_replica, values = 'replica domain', names = 'index', title= 'Replica domain')
                st.plotly_chart(fig, use_container_width=True)
            if genre == 'Images':
                liste_images_url = data_item['replica image'].tolist()
                st.image(liste_images_url, width = 100)

            if genre == 'Affluence/Price/Age':
                data_affluence = data_item
                data_affluence["replica is_green_website"] = [boolean_string(green) for
                                                              green in data_item["replica is_green_website"]]
                data_affluence['rank'] = [round(pop,2) for pop in data_item['rank']]
                data_affluence['replica website_age_in_months'] = \
                    [round(age/12.,2) for age in data_item['replica website_age_in_months']]
                fig = px.scatter(data_affluence,
                                 labels = {"replica price": 'Replica price',
                                          "replica website_age_in_months" : 'Web site age (year)',
                                          "replica is_green_website" : "Replica is green web site",
                                          "rank" : "Site afluence"
                                     },
                                 x="replica price",
                                 y="replica website_age_in_months",
                                 size="rank",
                                 color="replica is_green_website",
                                 title= 'Ancienneté, prix et afluence des réplicas',
                                 hover_name="replica domain", log_x=True, size_max=40)
                st.plotly_chart(fig, use_container_width=True)
                st.write("The circles represent all the replicas of the product" + \
                         ". The size of the circles is defined according to the afluence of the sites" + \
                             ",  the color indicates if the site is" + \
                             " reliable (Green) or not." )


        if st.sidebar.checkbox("Analysis by Product Class"):
            st.title('Analysis by Product Class')
            st.subheader('Price distribution and age of products by class')
            data_classe = classe_anova_replica(data)

            col_bar1, col_bar2 = st.columns([1,2])       
            with col_bar1:
                masque_prix = st.slider(
                'Plage des prix',
                0, 1000, (0, 500))

            vue_ensemble_data(data_classe,masque_prix[0],masque_prix[1])
            box_lien = "[box plot]" + '( https://en.wikipedia.org/wiki/Box_plot )'
            regression_lien = "[regression]" + '(https://en.wikipedia.org/wiki/Linear_regression )'

            st.markdown("Each dot represents the age and price of a product, the colors represent the" +
                     " different classes. A "+regression_lien+" line is drawn to express the general trends")
            st.markdown("- Right: distribution of the age of the products by a  " + box_lien)
            st.markdown("- Top: distribution of the product price by a "+ box_lien)

            st.subheader('Characteristics of the replica sites according to the product class')
            mode = st.radio("Type of analysis", ['Proportion Green Web Site replicas',
                                                           'Proportion Shopify replicas'])
            #'Ecart prix relatif' possible dans la select box mais Nan 

            fig = px.box(data_classe, y="Product class", x= mode ,color = "Product class",
                         color_discrete_sequence=['grey','green','orange'],
                         orientation = 'h',
                         points = 'all')
            fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('For a product we calculate the proportion of Green site (or shopify) of ' +
                        ' its replicas. A point represents this proportion according to the class of the product')
            st.markdown('A '+box_lien+ ' is added to view the statistical indicators')

            #calcul_correlation_anova(data_classe,mode)

    #%%
    ### VII - PROGRAMME PRINCIPAL
    interface()
