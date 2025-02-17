import streamlit as st

# st.set_page_config(layout="wide")

from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import requests
import pandas as pd
import numpy as np
import humanize
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)

from charts import line_chart, line_chart
from exchange_rates import get_exchange_rates

connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

count = st_autorefresh(interval=10 * 1000, limit=100, key="data_refresh")

engine = create_engine(connection_string)


def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df = df.set_index("timestamp")
    return df


def layout():
    
    st.title("Kryptokollen Dashboard")

    choice = st.radio("Choose Blockchain", ("Ethereum", "Solana"))

    selected_currency = st.radio("Choose currency", ["EUR", "SEK", "NOK", "DKK"])
    rates = get_exchange_rates()
    st.write("Rates:", rates)
    if rates is not None:
        conversion_rate = rates.get(selected_currency, 1.0)
    else:
        conversion_rate = 1.0

    if choice == "Ethereum":
        st.write("## Latest Ethereum Raw Data")
        
        df = load_data(
            """
            SELECT timestamp, coin, price_eur, volume_24h, percent_change_24h, percent_change_30d, market_cap FROM ethereum;
            """
        )

        df['price_eur'] = df['price_eur'].round(2)
        df['price_in_currency'] = df['price_eur'] * conversion_rate
        df['percent_change_24h'] = df['percent_change_24h'].round(1)
        df['percent_change_30d'] = df['percent_change_30d'].round(1)
        df['volume_24h'] = df['volume_24h'].apply(np.floor)
        df['market_cap'] = df['market_cap'].apply(np.floor)

        st.dataframe(df.tail())

        st.markdown("## Ethereum KPIs")

        col1, col2, col3, col4 = st.columns(4)

        volume_24h_value = int(df["volume_24h"].iloc[-1])
        formatted_volume_24h = humanize.intword(volume_24h_value)
        formatted_volume_24h = formatted_volume_24h.replace(" billion", "B").replace(" million", "M").replace(" thousand", "K")

        market_cap_value = int(df["market_cap"].iloc[-1])
        formatted_market_cap = humanize.intword(market_cap_value)
        formatted_market_cap = formatted_market_cap.replace(" billion", "B").replace(" million", "M").replace(" thousand", "K")

        col1.metric("Percent Change 24h", f"{df['percent_change_24h'].iloc[-1]}%")
        col2.metric("Percent Change 30d", f"{df['percent_change_30d'].iloc[-1]}%")
        col3.metric("Volume 24h", formatted_volume_24h)
        col4.metric("Market Cap", formatted_market_cap)

        st.markdown(f"## Ethereum (ETH) price in {selected_currency}")
        price_chart = line_chart(x=df.index, y=df["price_in_currency"], title=f"Price in {selected_currency}")
        st.pyplot(price_chart, bbox_inches="tight")

    elif choice == "Solana":
        st.write("## Latest Solana Raw Data")
        
        df = load_data(
            """
            SELECT timestamp, coin, price_eur, volume_24h, percent_change_24h, percent_change_30d, market_cap FROM solana;
            """
        )

        df['price_eur'] = df['price_eur'].round(2)
        df['price_in_currency'] = df['price_eur'] * conversion_rate
        df['percent_change_24h'] = df['percent_change_24h'].round(1)
        df['percent_change_30d'] = df['percent_change_30d'].round(1)
        df['volume_24h'] = df['volume_24h'].apply(np.floor)
        df['market_cap'] = df['market_cap'].apply(np.floor)

        st.dataframe(df.tail())

        st.markdown("## Solana KPIs")

        col1, col2, col3, col4 = st.columns(4)

        volume_24h_value = int(df["volume_24h"].iloc[-1])
        formatted_volume_24h = humanize.intword(volume_24h_value)
        formatted_volume_24h = formatted_volume_24h.replace(" billion", "B").replace(" million", "M").replace(" thousand", "K")

        market_cap_value = int(df["market_cap"].iloc[-1])
        formatted_market_cap = humanize.intword(market_cap_value)
        formatted_market_cap = formatted_market_cap.replace(" billion", "B").replace(" million", "M").replace(" thousand", "K")

        col1.metric("Percent Change 24h", f"{df['percent_change_24h'].iloc[-1]}%")
        col2.metric("Percent Change 30d", f"{df['percent_change_30d'].iloc[-1]}%")
        col3.metric("Volume 24h", formatted_volume_24h)
        col4.metric("Market Cap", formatted_market_cap)

        st.markdown(f"## Solana (SOL) price in {selected_currency}")
        price_chart = line_chart(x=df.index, y=df["price_in_currency"], title=f"Price in {selected_currency}")
        st.pyplot(price_chart, bbox_inches="tight")

if __name__ == "__main__":
    layout()
