from nltk.tokenize import RegexpTokenizer


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
        'SIRET',
        'Siret',
        'siret',
        'établissement',
        'numéro',
        'n°'    
    ]

    # Removal of punctuation and spaces
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(html)

    # Empty the variable to rewrite it
    html = ""

    # All characters are concatenated without punctuation or spaces
    for token in tokens:
        html += token

    num_siret = "null"

    for terme in liste_terme:
        if terme in html:
            num_siret = ""
            try:
                siret = html.find(terme)
                for caractere in range(siret + len(terme), siret + len(terme) + 14):
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
        'SIREN',
        'Siren',
        'siren',
        'RCS',
        'numéro',
        'n°'    
    ]

    # Removal of punctuation and spaces
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(html)

    # Empty the variable to rewrite it
    html = ""

    # All characters are concatenated without punctuation or spaces
    for token in tokens:
        html += token

    num_siren = "null"

    for terme in liste_terme:
        if terme in html:
            num_siren = ""
            try:
                siren = html.find(terme)
                for caractere in range(siren + len(terme), siren + len(terme) + 9):
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
            tva = ""
            try:
                num_tva = html.find(code_iso)
                for caractere in range(num_tva + len(code_iso), num_tva + len(code_iso) + 11):
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
