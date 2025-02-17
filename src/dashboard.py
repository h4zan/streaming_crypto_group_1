import streamlit as st
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)

from charts import line_chart, line_chart
from exchange_rates import CURRENCIES

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

    if choice == "Ethereum":
        selected_currency = st.radio("Choose currency", CURRENCIES)
        st.write("## Latest Ethereum Data")
        
        df = load_data(
        f"""
            SELECT timestamp, coin, price_eur, volume_24h, percent_change_24h, market_cap FROM ethereum;
        """)

        df['price_eur'] = df['price_eur'].round(2)
        df['percent_change_24h'] = df['percent_change_24h'].round(1).astype(str) + '%'
        df['volume_24h'] = df['volume_24h'].apply(np.floor)
        df['market_cap'] = df['market_cap'].apply(np.floor)

        st.dataframe(df.tail())

        st.markdown(f"## Ethereum (ETH) price in {selected_currency}")

        price_chart = line_chart(x=df.index, y=df["price_eur"], title = selected_currency)

        st.pyplot(price_chart, bbox_inches="tight")

        price_chart = line_chart(
            x=df.index,
            y=df["price_eur"],
            title=f"Price {selected_currency}",
        )



    elif choice == "Solana":
        selected_currency = st.radio("Choose currency", CURRENCIES)
        st.write("## Latest Solana Data")
        
        df = load_data(""" SELECT * FROM solana;""")

        st.dataframe(df.tail())

        st.markdown(f"## Solana (SOL) price in {selected_currency}")

        price_chart = line_chart(x=df.index, y=df["price_eur"], title = selected_currency)

        st.pyplot(price_chart, bbox_inches="tight")

        price_chart = line_chart(
            x=df.index,
            y=df["price_eur"],
            title=f"Price {selected_currency}",
        )

if __name__ == "__main__":
    layout()
