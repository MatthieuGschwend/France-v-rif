# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:02:28 2021

@author: Matthieu
"""

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

    def liste_item(data):
        '''renvoie la liste des items '''
        return data['product name'].unique()

    def liste_replica(data_item):
        ''' renvoie la liste des réplicas pour un item'''
        return data_item['replica name'].unique()

    def camembert(data, valeurs, noms ):
        '''renvoie un camembert : propotion des valeurs selon les noms '''
        fig = px.pie(data, values = valeurs, names = noms, title='Population of European continent')
        st.plotly_chart(fig, use_container_width=True)

    def info_generale_replica(data_item):
        nb_replicas = data_item.shape[0]
        replica_green_moy = data_item['replica is_green_website'].mean()
        affluence_moy = data_item['rank'].mean()
        prix_moyen = data_item['replica price'].mean() 
        return df

    def boolean_string(oui_ou_non):
        if(oui_ou_non == 1):
            return 'Yes'
        else : 
            return 'No'

    def affichage_image(data_item):
        try:
            product_image = data_item['product image'].values[0]
            return st.image(product_image, width = 200)
        except:
            pass

    def affichage_prix(data_item):
        try:
            product_prix = str(data_item['product price'].values[0])
            return st.markdown('- Price : ' + product_prix +' euros' )
        except:
            pass

    def affichage_site(data_item):
        try:
            product_web_site  = data_item['product domain'].values[0]
            product_web_site = "["+product_web_site +"]" + '(https://' + product_web_site + ')'
            return st.markdown('- Web Site : ' + product_web_site)
        except:
            pass

    def affichage_url(data_item):
        try:
            product_url  = data_item['product url'].values[0]
            product_url = "[Lien du produit]" + '(' + product_url + ')'
            return st.markdown(product_url)
        except:
            pass

    def affichage_anciennete(data_item):
        try:
            product_age_months = data_item['product website_age_in_months']\
                                     .values[0]
            return st.markdown('- Age : ' + mois_annees(product_age_months))
        except:
            pass

    def affichage_shopify(data_item):
        try:
            product_shopify = data_item['product is_shopify'].values[0]
            return st.markdown('- Shopify : ' + boolean_string(product_shopify))
        except:
            pass

    def affichage_green(data_item):
        try:
            product_green = data_item['product is_green_website'].values[0]
            return st.markdown('- Reliable : ' + boolean_string(product_green))
        except:
            pass

    def affichage_classe(data_item):
        try:
            product_class = data_item['product class'].values[0]
            return st.markdown('- Product class : ' + product_class)
        except:
            pass

    def affichage_description(data_item):
        try:
            product_description = data_item['product description'].values[0]
            return st.text_area('Description',value = product_description, height = 180)
        except:
            pass


    def affichage_replica_image(data_item,replica_name):
        try:
            replica_image = data_item[data_item['replica name']==replica_name]\
                ['replica image'].values[0]
            return st.image(replica_image, width = 200)
        except:
            pass

    def affichage_replica_prix(data_item, replica_name):
        try:
            replica_prix = data_item[data_item['replica name']==replica_name]\
                ['replica price'].values[0]
            replica_prix = str(replica_prix)
            return st.markdown('- Price : ' + replica_prix +' euros')
        except:
            pass

    def affichage_replica_site(data_item, replica_name):
        try:
            replica_site = data_item[data_item['replica name']==replica_name]\
                ['replica domain'].values[0]
            replica_site = "["+replica_site +"]" + '(https://' + replica_site + ')'
            return st.markdown('- Web site : ' + replica_site)
        except:
            pass

    def affichage_replica_url(data_item, replica_name):
        try:
            replica_url = data_item[data_item['replica name']==replica_name]\
                ['replica url'].values[0]
            replica_url = "[replica link]" + '(' + replica_url + ')'
            return st.markdown(replica_url)
        except:
            pass


    def affichage_replica_anciennete(data_item, replica_name):
        try:
            replica_age = data_item[data_item['replica name']==replica_name]\
                ['replica website_age_in_months'].values[0]
            return st.markdown('- Age : ' + mois_annees(replica_age))
        except:
            pass

    def affichage_replica_shopify(data_item, replica_name):
        try:
             replica_shopify = data_item[data_item['replica name']==replica_name]\
                ['replica is_shopify'].values[0]
             return st.markdown('- Shopify : ' + boolean_string(replica_shopify))
        except:
            pass

    def affichage_replica_green(data_item, replica_name):
        try:
            replica_green = data_item[data_item['replica name']==replica_name]\
                ['replica is_green_website'].values[0]
            return st.markdown('- Green web site : ' + boolean_string(replica_green))
        except:
            pass

    def affichage_replica_description(data_item, replica_name):
        try:
            replica_description = data_item[data_item['replica name']==replica_name]\
                ['replica description'].values[0]
            return st.text_area('Description',value = replica_description, height = 180)
        except:
            pass



    #%% Analyse ANOVA globale
    @st.cache
    def classe_anova_replica(data):

        ''' Pour tous les produits nous voulons faires des analyses de
        corrélation entre le label final (product class) avec les propriétés des 
        réplicas : prix des réplicas, proportion de sites Green, proportion de 
        site shopify'''

        liste_item = data['product name'].unique() # liste des produits

        def ecart_moy_prix_replica(nom_produit, data):
            '''Pour chaque produit nous voulons avoir le prix des réplicas,
            en particulier l'écart moyen avec le prix original. Nous divisons cette 
            différence par le prix original pour avoir des valeurs homogènes '''

            data_item = data[data['product name'] == nom_produit]
            prix_item = data_item['product price'].values[0]
            liste_ecarts_prix = data_item['replica price']

            return (liste_ecarts_prix - prix_item).mean()/prix_item

        def moy_site_green_replica(nom_produit, data):
            '''Proportion de site green dans les réplicas d'un produit'''
            data_item = data[data['product name'] == nom_produit]
            return data_item['replica is_green_website'].mean()

        def moy_shopyfi_replica(nom_produit, data):
            '''Proportion de site shopyfi dans les réplicas d'un produit'''
            data_item = data[data['product name'] == nom_produit]
            return data_item['replica is_shopify'].mean()

        def classe_item(nom_produit, data):
            data_item = data[data['product name'] == nom_produit]
            return data_item['product class'].values[0]

        def age_article(nom_produit, data):
            data_item = data_item = data[data['product name'] == nom_produit]
            return data_item['product website_age_in_months'].values[0]

        def prix_article(nom_produit, data):
            data_item = data_item = data[data['product name'] == nom_produit]
            return data_item['product price'].values[0]


        # Construction d'un data frame avec toutes les infos 
        # 1 - valeurs des colonnes : 
        prix_moyen = [ecart_moy_prix_replica(nom,data) for nom in liste_item]
        green_moyen = [moy_site_green_replica(nom,data) for nom in liste_item]
        shopify_moyen = [moy_shopyfi_replica(nom,data) for nom in liste_item]
        label_item = [classe_item(nom, data) for nom in liste_item]
        age_article = [age_article(nom, data) for nom in liste_item]
        article_prix = [prix_article(nom, data) for nom in liste_item]

        df = pd.DataFrame({'Product name':liste_item,
                               'Relative price differential': prix_moyen,
                               'Proportion Green Web Site replicas': green_moyen, 
                               'Proportion Shopify replicas': shopify_moyen,
                               'Product class' : label_item,
                               'Age' : age_article,
                               'Product price': article_prix
                               })

        # fig = px.box(df, x="Classe du produit", y="Porportion Shopify",color = "Classe du produit")
        # fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        # st.plotly_chart(fig, use_container_width=True)

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
        for classe in data_classe['Product class'].unique():
            val_classe = data_classe[data_classe['Product class'] == classe][var_qualitative]
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


        if st.sidebar.checkbox("Collected data"):

            #mode = st.sidebar.selectbox('Liste des items',np.insert(liste_items,0," "))
            st.title("Collected data")
            #st.write(data_item)
            #st.subheader(str(mode))
            col1, col2 = st.columns(2)
            with col1:
                st.header('Initial product')
                liste_items = liste_item(data)
                mode = st.selectbox('Produits list', liste_items)
                data_item = data[data['Product name'] == mode]
                affichage_image(data_item)

            with col2:
                st.header('Replicas')
                liste_replicas = liste_replica(data_item)
                replica_name = st.selectbox('Replicas list', liste_replicas)
                affichage_replica_image(data_item,replica_name)


            col3, col4 = st.columns(2)
            with col3:
                affichage_url(data_item)
                affichage_description(data_item)
                affichage_prix(data_item)
                affichage_site(data_item)
                affichage_green(data_item)
                affichage_anciennete(data_item)
                affichage_shopify(data_item)
                affichage_classe(data_item)


            with col4:
                affichage_replica_url(data_item,replica_name)
                affichage_replica_description(data_item,replica_name)
                affichage_replica_prix(data_item,replica_name)
                affichage_replica_site(data_item,replica_name)
                affichage_replica_green(data_item,replica_name)
                affichage_replica_anciennete(data_item,replica_name)
                affichage_replica_shopify(data_item,replica_name)



            st.header("Information on all replicas")
            col5, col6 = st.columns([1, 2])
            with col5:
                st.markdown('-  Number of replicas : ' +  str(round(data_item.shape[0],2)))
                st.markdown('- Average price : ' +  str(round(data_item['replica price'].mean(),2)) )
                st.markdown('- Green site web (%) : '  + 
                        str(round(data_item['replica is_green_website'].mean() * 100,2)))
                st.markdown('- Average attendance : ' +  str(round(data_item['rank'].mean(),2)))

            with col6:
                genre = st.radio("Additional visualization",('Domains', 
                                                                 'Affluence/Price/Age', 'Images'))
            if genre == 'Domaines':
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

            st.markdown('Pour un produit nous calculons la proportion de site Green (ou shopify) de' +
                        ' ses réplicas. Un point représente cette proportion selon la classe du produit')
            st.markdown('Un '+box_lien+ ' est ajouté pour visualiser les indicateurs statistiques')

            calcul_correlation_anova(data_classe,mode)

    #%%
    ### VII - PROGRAMME PRINCIPAL
    interface()