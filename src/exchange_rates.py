import json
import requests
import streamlit as st
from constants import EXCHANGE_RATE_API

@st.cache_data(ttl=21600)
def get_exchange_rates():
    conversion_api = f"http://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_RATE_API}&symbols=SEK,NOK,DKK,EUR"
    response = requests.get(conversion_api)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data.get("rates")
    else:
        st.error(f"Error fetching exchange rates: {response.status_code}")
        return None