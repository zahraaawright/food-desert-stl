"""Streamlit dashboard: food desert scores by St. Louis census tract."""
import pandas as pd
import streamlit as st
from google.cloud import bigquery

st.set_page_config(page_title="St. Louis food deserts", layout="wide")
st.title("St. Louis food access by census tract")

client = bigquery.Client()

@st.cache_data(ttl=3600)
def load_scores() -> pd.DataFrame:
    query = """
        select tract, tract_name, median_household_income,
               total_population, nearby_grocery_count
        from `food_desert.food_desert_scores`
    """
    return client.query(query).to_dataframe()

df = load_scores()

st.dataframe(df, use_container_width=True)
st.bar_chart(df.set_index("tract_name")["nearby_grocery_count"])
