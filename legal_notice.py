import time
import pandas as pd
import asyncio
import aiohttp
import html2text
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from extraction_info import find_siret, find_siren, find_strange_address, find_mediator, find_tva


# Headers to simulate a browser for the requests parameter
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/88.0.4324.150 Safari/537.36',
}


class Http:
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get_raw(self, url, **kwargs):
        async with self._session.get(url, **kwargs) as resp:
            try:
                resp.raise_for_status()
                return await resp.content.read(), resp
            except:
                return None, resp


async def get_aiohttp_res(url, req_option):
    async with Http() as http:
        text_res, full_resp = await http.get_raw(url, **req_option)
        return text_res, full_resp


async def main_legal_notice(url_to_analyze: str):
    """
    Example of url_to_analyze: 'ebay.fr'
    """
    print(url_to_analyze)
    url_to_analyze = url_to_analyze.replace('http://', '')
    url_to_analyze = url_to_analyze.replace('https://', '')
    url_to_analyze = url_to_analyze.replace('www.', '')    

    # Time measurement for algorithm benchmarking
    start = time.perf_counter()

    # Dictionary initialization
    dictionary = {
        'url': [], # str
        'response': [], # int
        'legal_notice_url': [], # str
        'legal_notice': [], # str (converted to bool before exporting to csv)
        'character_nb': [], # int
        'siret': [], # int
        'siren': [], # int
        'vat': [], # str
        'has_strange_address': [], # bool
        'triggered_strange_address' : [], # str
        'has_mediator': [] # bool
    }

    dictionary["url"]

    # List of strange countries
    country_list = ['New Mexico', 'Nouveau Mexique', 'Wyoming', 'Nevada',
    'Delaware', 'Dubaï', 'Dubai', 'United Arab Emirates',
    'Emirats Arabes Unis', 'Bahamas', 'Seychelles', 'Belize',
    'Cayman Island', 'Iles Cayman', 'Îles Cayman', 'Thailand', 'Thailande',
    'Vietnam', 'Ukraine', 'Russie', 'Russia', 'Malaysia', 'Malaisie',
    'Cambodge', 'Cambodia', 'Indonesia', 'Indonesie', 'Bali', 'Inde',
    'India', 'Pakistan', 'Bangladesh', 'Hong Kong']

    liste_sites = []
    liste_sites.append(url_to_analyze)

    clean_url = []
    for url in liste_sites:
        url = url.strip()
        url = 'http://www.' + url
        clean_url.append(url)

    options = {
    "headers": headers,
    "timeout": 10,
    "allow_redirects":True
    }
    tasks = []
    tasks += [get_aiohttp_res(clean_url[0], options)]
    responses1 = await asyncio.gather(*tasks)

    successful_results = []
    success_code = []
    bad_results = []
    bad_code = []
    for result, url in zip(responses1, clean_url):
        text_result, full_resp = result
        status_code = full_resp.status
        if not text_result:
            bad_results.append(url)
            bad_code.append(status_code)
        elif not str(status_code).startswith("2"):
            bad_results.append(url)
            bad_code.append(status_code)
        else:
            successful_results.append(result)
            success_code.append(status_code)

    all_codes = success_code
    all_codes.extend(bad_code)

    all_results = successful_results
    all_results.extend(bad_results)

    legal_related_terms = [
        'Mentions Légales', 'mentions légales',
        'Mentions Legales', 'mentions legales',

        'Mention Légales', 'mention légales',
        'Mention Legales', 'mention legales',

        'Mentions Légale', 'mentions légale',
        'Mentions Legale', 'mentions legale',
                            
        'Mentions légales', 'Mentions legales',

        'MENTIONS LÉGALES', 'MENTIONS LEGALES',

        'Legal Notice', 'legal notice',
        'Legal notice', 'legal Notice',

        'Info Éditeur', 'Infos Légales',

        'Legal', 'Légal', 'legal', 'légal'
        ]

    cgv_related_terms = [
        'cgv', 'CGV',

        'Conditions générales', 'Condition Générales',
        'CONDITIONS GÉNÉRALES', 'CONDITIONS GENERALES',
                
        'Conditions de vente', 'CONDITIONS DE VENTE'
        ]
                        
    # Searching of the legal notice url
    base_urls = []
    legal_notice_urls = []
    # print("Retreiving legal notice urls...")
    for result in all_results:
        text_result, full_resp = result
        try:
            url = str(full_resp.url)
            base_url = url.split('/')[2]
            bad_url = False
        except:
            url = str(full_resp.url)
            base_url = url.split('/')[2]
            bad_url = True
        if not bad_url:
            html = BeautifulSoup(text_result, 'html.parser')
            href_tags = html.find_all(href=True)
            legal_notice_url = None
            for lien in href_tags:
                href_text = lien.text
                href = lien.get('href')
                for term in legal_related_terms:
                    if term in href_text:
                        legal_notice_url = href
                        break
                    else:
                        continue

                if legal_notice_url == None:
                    for term in cgv_related_terms:
                        if term in href_text:
                            legal_notice_url = href
                            break

            if legal_notice_url is not None:
                legal_notice_url = legal_notice_url.replace('https', 'http')
                legal_notice_url = legal_notice_url.replace('www.', '')
                legal_notice_url = legal_notice_url.replace(url, '')
                if legal_notice_url.startswith("/"):
                    legal_notice_url =  url[0:-1] + legal_notice_url
                elif not legal_notice_url.startswith("http") and not legal_notice_url.startswith("/"):
                    legal_notice_url = "http://" + base_url + "/" + legal_notice_url
                legal_notice_urls.append(legal_notice_url)
                base_urls.append(base_url)
            else:
                base_urls.append(base_url)
                legal_notice_urls.append(base_url)
        else:
            base_urls.append(base_url)
            legal_notice_urls.append(base_url)        

    # Requests of the legal notice urls found
    # requests_legal = [grequests.get(link, headers=headers, timeout=10) for link in legal_notice_urls]
    # responses_legal = grequests.map(requests_legal)
    print(legal_notice_urls)
    tasks = []
    tasks += [get_aiohttp_res(link, options) for link in legal_notice_urls]
    responses_legal = await asyncio.gather(*tasks)


    def nettoyage(html: str):
        """Get the text of html page by setting the url in the paramater.
        Converts the html page into text by removing everything that is not text
        (html tags, css code...).

        Parameters
        ----------
        url: url of the html page we want to have.

        Returns
        ----------
        clean_html (str): Return only the text of the html page.
        length (int): Length of the html text (length of clean_html).
        """
        try:
            html = BeautifulSoup(html, features="lxml").get_text()
            clean_html = html2text.html2text(html)
            clean_html = clean_html.strip()
            length = len(clean_html)
        except:
            clean_html = 'null'
            length = 0

        return clean_html, length


    async def main(base_url, response, code):
        base_url = base_url.replace('www.', '')
        html, full_resp = response
        if html is None:
            url_legal_notice = base_url
        else:
            url_legal_notice = str(full_resp.url)
        clean_html, length = nettoyage(html)
        dictionary['legal_notice_url'].append(url_legal_notice)
        dictionary['legal_notice'].append(clean_html)
        dictionary['character_nb'].append(length)
        dictionary['siret'].append(find_siret(clean_html))
        dictionary['siren'].append(find_siren(clean_html))
        dictionary['vat'].append(find_tva(clean_html))
        has_strange_adress, country = find_strange_address(clean_html, country_list)
        dictionary['has_strange_address'].append(has_strange_adress)
        dictionary['triggered_strange_address'].append(country)
        dictionary['has_mediator'].append(find_mediator(clean_html))
        dictionary['url'].append(base_url)
        dictionary['response'].append(code)

    # with ThreadPoolExecutor() as executor:
    #     _ = [executor.submit(main, base_url, response, code)
    #     for base_url, response, code in zip(base_urls, responses_legal, all_codes)]

    tasks = []
    tasks += [main(base_url, response, code)
        for base_url, response, code in zip(base_urls, responses_legal, all_codes)]
    await asyncio.gather(*tasks)

    # Conversion of the dictionary into a dataframe table
    data = pd.DataFrame(dictionary)

    # Conversion to bool
    data['legal_notice'] = data['legal_notice'] != "null"

    # Sorting of the table
    data = data.sort_values(by='response', ascending=True)
    data = data.sort_values(by='legal_notice', ascending=False)

    # Column renaming
    data = data.rename(columns={
        "legal_notice": "found_legals",
        "siret": "has_siret",
        "siren": "has_siren",
        "vat": "has_vat"
    })

    # # Cleaning url columns as multithreading method is messing up the data
    # urls_list = data['legal_notice_url'].to_list()
    # clean_list_url = []
    # clean_list_legal = []
    # for url in urls_list:
    #     if "/" in url:
    #         clean_list_legal.append(url)
    #         url = url.split('/')
    #         url = url[2]
    #     else:
    #         clean_list_legal.append('null')
    #     url = url.replace('www.', '')
    #     clean_list_url.append(url)

    # data['url'] = clean_list_url
    # data['legal_notice_url'] = clean_list_legal

    # Converting dataframe to dictionary
    dictionary = data.to_dict('records')
    dictionary = dictionary[0]

    finish = time.perf_counter()
    formated_time = time.strftime('%Hh%Mm%Ss', time.gmtime(finish-start))
    # print(f'\nFinished in {formated_time}')

    return dictionary
