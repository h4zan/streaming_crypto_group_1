import streamlit as st
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
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
        # print(df)
        df = df.set_index("timestamp")
    return df


def layout():

    selected_currency = st.selectbox("Choose currency", CURRENCIES)

    df = load_data(
        """
                SELECT * FROM ethereum;
                """
    )
    st.markdown("# Ethereum")
    st.markdown("## Latest data")

    st.dataframe(df.tail())

    st.markdown(f"## Ethereum (ETH) latest price in {selected_currency}")

    price_chart = line_chart(x=df.index, y=df["price_eur"], title = selected_currency)

    st.pyplot(price_chart, bbox_inches="tight")

# def layout():

#     selected_currency = st.selectbox("Choose currency", CURRENCIES)

#     df = load_data(
#         f"""
#             SELECT timestamp, coin, ROUND((price_usd * {CURRENCIES[selected_currency]})::NUMERIC, 2) as price, volume FROM ordi;
#         """
#     )
#     st.markdown("# Ordi data")
#     st.markdown(f"## Latest data (in {selected_currency})")

#     st.dataframe(df.tail(10))

#     st.markdown(f"## Ordi latest price in {selected_currency}")

    price_chart = line_chart(
        x=df.index,
        y=df["price_eur"],
        title=f"Price {selected_currency}",
    )


if __name__ == "__main__":
    layout()
