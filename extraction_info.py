from nltk.tokenize import RegexpTokenizer
import re
import streamlit as st


def find_siret(html:str):
    """
    Get the Siret from a text.

    Parameters
    ----------
    html: Text of the html page.

    Returns
    ----------
    has_siret (bool): True if the siret has been found, else, False.
    """
    # List of related terms to 'Siret'
    liste_terme = [
        'siret',
        'établissement',
        'numéro',
        'n°',
        'n°suivant',
        'siren' 
    ]

    # We put everything in lower case
    html = html.lower()

    # Removal of punctuation and spaces
    # '\w+' matches any word character (equal to [a-zA-Z0-9_])
    tokenizer = RegexpTokenizer(r'°|\w+')
    tokens = tokenizer.tokenize(html)

    # Empty the variable to rewrite it
    html = ""

    # All characters are concatenated without punctuation or spaces
    for token in tokens:
        html += token

    num_siret = "null"

    for terme in liste_terme:
        if terme in html:
            all_occurences = [
                string.start() for string in re.finditer(terme, html)]
            for occurrence in all_occurences:
                num_siret = ""
                try:
                    for caractere in range(
                        occurrence + len(terme),
                        occurrence + len(terme) + 14):
                        num_siret += str(html[caractere])
                    num_siret = int(num_siret)
                    return num_siret
                except:
                    num_siret = "null"
                    continue

    return num_siret                      


def find_siren(html:str):
    """
    Get the siren from a text

    Parameters
    ----------
    html: Text of the html page.

    Returns
    ----------
    has_siren (bool): True if the siren has been found, else, False.
    """
    # List of terms related to 'Siren'
    liste_terme = [
        'siren',
        'rcs',
        'numéro',
        'n°',
        'n°suivant',
        'siret'
    ]

    # We put everything in lower case
    html = html.lower()

    # Removal of punctuation and spaces
    tokenizer = RegexpTokenizer(r'°|\w+')
    tokens = tokenizer.tokenize(html)

    # Empty the variable to rewrite it
    html = ""

    # All characters are concatenated without punctuation or spaces
    for token in tokens:
        html += token

    num_siren = "null"

    for terme in liste_terme:
        if terme in html:
            # start(): tells the index of the starting position of the match.
            all_occurences = [
                string.start() for string in re.finditer(terme, html)]
            for occurrence in all_occurences:
                num_siren = ""
                try:
                    for caractere in range(
                        occurrence + len(terme),
                        occurrence + len(terme) + 9):
                        num_siren += str(html[caractere])
                    num_siren = int(num_siren)
                    return num_siren
                except:
                    num_siren = "null"
                    continue

    return num_siren


def find_tva(html:str):
    """
    Get the vat number of a text.

    Parameters
    ----------
    html: Text of the html page.

    Returns
    ----------
    has_tva (bool): True if VAT has been found, else, False.
    """
    # List of country iso codes for VAT numbers
    liste_code = [
        'FR',
        'DE',
        'BE',
        'IT',
        'GB',
        'NL',
        'ES'  
    ]

    # Removal of punctuation and spaces
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(html)

    # Empty the variable to rewrite it
    html = ""

    # All characters are concatenated without punctuation or spaces
    for token in tokens:
        html += token
        
    tva = "null"
    for code_iso in liste_code:
        if code_iso in html:
            # start(): tells the index of the starting position of the match.
            all_occurences = [
                string.start() for string in re.finditer(code_iso, html)]
            for occurrence in all_occurences:
                tva = ""
                try:
                    # num_tva = html.find(code_iso)
                    for caractere in range(
                        occurrence + len(code_iso),
                        occurrence + len(code_iso) + 11):
                        tva += str(html[caractere])
                    tva = int(tva) # To verify if we get an integer or not
                    tva = code_iso+str(tva)
                    return tva
                except:
                    tva = "null"
                    continue

    return tva


def find_strange_address(html:str, pays:list):
    """
    Look for a "strange" country in the text.
    Parameters
    ----------
    html: Text of the html page.
    pays: List of countries considered as "strange" if they are in the
    address.

    Returns
    ----------
    has_strange_adress (bool): True if one of the country from the list has
    been found in the page, else, False.
    strange_pays (str): Country that triggered the True value of the variable
    'has_strange_adress'.
    """
    html = html.replace('Hong Kong', 'HongKong')
    html = html.replace('New Mexico', 'NewMexico')
    html = html.replace('United Arab Emirates', 'UnitedArabEmirates')
    html = html.replace('Emirats Arabes Unis', 'EmiratsArabesUnis')
    html = html.replace('Cayman Island', 'CaymanIsland')
    html = html.replace('Iles Cayman', 'IlesCayman')
    html = html.replace('Îles Cayman', 'ÎlesCayman')

    # Removal of punctuation and spaces
    tokenizer = RegexpTokenizer(r'\w+')
    # Adding words to a list
    words_list = tokenizer.tokenize(html)

    for strange_pays in pays:
        strange_pays = strange_pays.strip()
        if strange_pays in words_list:
            has_strange_adress = True
            return has_strange_adress, strange_pays
        else:
            strange_pays = 'null'
            has_strange_adress = False

    return has_strange_adress, strange_pays


def find_mediator(html:str):
    """
    Look for the word "médiateur" in the text.
    """
    if "médiateur" in html:
        mediator = True
    else:
        mediator = False

    return mediator
