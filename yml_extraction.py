import streamlit as st
from selectorlib import Extractor
from io import StringIO
import asyncio
import aiohttp


def app():
    class Http:
        async def __aenter__(self):
            self._session = aiohttp.ClientSession()
            return self

        async def __aexit__(self, *err):
            await self._session.close()
            self._session = None

        async def get(self, url, **kwargs):
            async with self._session.head(url, **kwargs) as resp:
                await resp.read()
                return resp

        async def get_json(self, url, **kwargs):
            async with self._session.get(url, **kwargs) as resp:
                resp.raise_for_status()
                return await resp.json()

        async def post_json(self, url, **kwargs):
            async with self._session.post(url, **kwargs) as resp:
                resp.raise_for_status()
                return await resp.json()

        async def get_raw(self, url, **kwargs):
            async with self._session.get(url, **kwargs) as resp:
                resp.raise_for_status()
                return await resp.read()

        async def post_raw(self, url, **kwargs):
            async with self._session.post(url, **kwargs) as resp:
                resp.raise_for_status()
                return await resp.read()


    async def get_html_code(url):
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
                    'AppleWebKit/537.36 (KHTML, like Gecko) '\
                    'Chrome/91.0.4472.124 '\
                    'Safari/537.36'
    }
        options = {
            "headers": headers,
            "timeout": 5,
            "allow_redirects":True
        }   
        try:
            async with Http() as http:
                content = await http.get_raw(url, **options)
                content = content.decode()
        except Exception as e:
            st.error(f"failed {url} with {e} ")
            content = None
        return content


    product_page_url = st.text_input("Product page url")
    if product_page_url:
        content = asyncio.run(get_html_code(product_page_url))

    uploaded_file = st.file_uploader("Choose a yml file")

    if product_page_url and uploaded_file:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()

        extractor = Extractor.from_yaml_string(string_data)
        data = extractor.extract(content)
        st.write(data)