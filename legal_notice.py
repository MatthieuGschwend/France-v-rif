import pandas as pd
import tqdm
import sys
import asyncio
import aiohttp
import html2text
from bs4 import BeautifulSoup
import streamlit as st
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
            resp.raise_for_status()
            return await resp.content.read(), resp
    

async def get_aiohttp_res(url, req_option):
    if "http" not in url:
        url = 'http://' + url
    async with Http() as http:
        try:
            text_res, full_resp = await http.get_raw(url, **req_option)
            return text_res, full_resp
        except:
            return None, None


async def main_legal_notice(url_to_analyze: str):
    """
    Example of url_to_analyze: 'ebay.fr'
    """
    url_to_analyze = url_to_analyze.replace('http://', '')
    url_to_analyze = url_to_analyze.replace('https://', '')
    url_to_analyze = url_to_analyze.replace('www.', '')    
    url_to_analyze = url_to_analyze.strip()
    url_to_analyze = 'http://www.' + url_to_analyze

    # dictionary initialization
    data = {
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

    data["url"]

    # List of strange countries
    country_list = ['New Mexico', 'Nouveau Mexique', 'Wyoming', 'Nevada',
    'Delaware', 'Duba??', 'Dubai', 'United Arab Emirates',
    'Emirats Arabes Unis', 'Bahamas', 'Seychelles', 'Belize',
    'Cayman Island', 'Iles Cayman', '??les Cayman', 'Thailand', 'Thailande',
    'Vietnam', 'Ukraine', 'Russie', 'Russia', 'Malaysia', 'Malaisie',
    'Cambodge', 'Cambodia', 'Indonesia', 'Indonesie', 'Bali', 'Inde',
    'India', 'Pakistan', 'Bangladesh', 'Hong Kong']

    options = {
    "headers": headers,
    "timeout": 10,
    "allow_redirects":True
    }

    response = await get_aiohttp_res(url_to_analyze, options)

    legal_related_terms = [
        'Mentions L??gales', 'mentions l??gales',
        'Mentions Legales', 'mentions legales',

        'Mention L??gales', 'mention l??gales',
        'Mention Legales', 'mention legales',

        'Mentions L??gale', 'mentions l??gale',
        'Mentions Legale', 'mentions legale',
                            
        'Mentions l??gales', 'Mentions legales',

        'MENTIONS L??GALES', 'MENTIONS LEGALES',

        'Legal Notice', 'legal notice',
        'Legal notice', 'legal Notice',

        'Info ??diteur', 'Infos L??gales',

        'Legal', 'L??gal', 'legal', 'l??gal'
        ]

    cgv_related_terms = [
        'cgv', 'CGV',

        'Conditions g??n??rales', 'Condition G??n??rales',
        'Conditions G??n??rales',
        'CONDITIONS G??N??RALES', 'CONDITIONS GENERALES',
                
        'Conditions de vente', 'CONDITIONS DE VENTE'
        ]
                        
    # Searching of the legal notice url
    base_urls = []
    legal_notice_urls = []
    # print("Retreiving legal notice urls...")

    text_result, full_resp = response
    # TODO: better catching of the code error
    if full_resp is None:
        data["response"] = 404
    else:
        data["response"] = full_resp.status

    try:
        url = str(full_resp.url)
        base_url = url.split('/')[2]
        bad_url = False
    except:
        url = url_to_analyze
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
            html = BeautifulSoup(
                html.decode('iso-8859-1','ignore'), features="lxml").get_text()
            clean_html = html2text.html2text(html)
            clean_html = clean_html.strip()
            length = len(clean_html)
        except:
            clean_html = 'null'
            length = 0

        return clean_html, length


    async def main(base_url, response):
        base_url = base_url.replace('www.', '')
        html, full_resp = response
        if html is None:
            url_legal_notice = base_url
        else:
            url_legal_notice = str(full_resp.url)
        clean_html, length = nettoyage(html)
        data['legal_notice_url'].append(url_legal_notice)
        data['legal_notice'].append(clean_html)
        data['character_nb'].append(length)
        data['siret'].append(find_siret(clean_html))
        data['siren'].append(find_siren(clean_html))
        data['vat'].append(find_tva(clean_html))
        has_strange_adress, country = find_strange_address(clean_html, country_list)
        data['has_strange_address'].append(has_strange_adress)
        data['triggered_strange_address'].append(country)
        data['has_mediator'].append(find_mediator(clean_html))
        data['url'].append(base_url)


    tasks = []
    tasks += [
        main(base_url, response) for base_url, response in
        zip(base_urls, responses_legal)
    ]
    await asyncio.gather(*tasks)

    # Conversion of the data into a dataframe table
    data = pd.DataFrame(data)

    # Conversion to bool
    data['legal_notice'] = data['legal_notice'] != "null"

    # Sorting of the table
    data = data.sort_values(by='legal_notice', ascending=False)

    # Column renaming
    data = data.rename(columns={
        "legal_notice": "found_legals",
        "siret": "has_siret",
        "siren": "has_siren",
        "vat": "has_vat"
    })

    # Converting dataframe to data
    data = data.to_dict('records')
    data = data[0]

    return data


class Collector():
    def batch(iterable, n=10):
        "Divide a list every n indices. Used to make asyncio tasks safer"
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

    async def collection(urls):

        """Returns a DataFrame"""
        # asynchronous by batch of 10 urls
        result = []
        print("list len: ", len(urls))
        for batch in tqdm.tqdm(Collector.batch(urls, 10), total=len(urls)//10):
            tasks = []
            for url in batch:
                tasks += [main_legal_notice(url)]
            result += [await f for f in asyncio.as_completed(tasks)]

        # sequential
        # result = []
        # for url in tqdm(urls):
        #     result += await main_legal_notice(url)

        return pd.DataFrame.from_records(result)


# urls = pd.read_csv("security-export - latest.csv")["domain"]
# urls = urls.dropna()
# urls = urls.drop_duplicates()
# urls = urls.to_list()

# https://github.com/encode/httpx/issues/914
# if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# res = asyncio.run(Collector.collection(urls))
# res.to_csv("mentions_legales_algo_test.csv", index=False)