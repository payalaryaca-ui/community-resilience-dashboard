

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Community Resilience Dashboard", layout="wide")

st.title("Community Resilience Dashboard")
st.caption("211 needs data normalized by population")

df = pd.read_csv("city_year_trends.csv")

cities = sorted(df["CityName"].dropna().unique())
categories = sorted(df["AIRSNeedCategory"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "Select communities",
    cities,
    default=cities[:5]
)

selected_categories = st.sidebar.multiselect(
    "Select need categories",
    categories,
    default=categories[:6]
)

filtered = df[
    (df["CityName"].isin(selected_cities)) &
    (df["AIRSNeedCategory"].isin(selected_categories)) &
    (df["year"].isin([2024, 2025]))
]

st.subheader("Year-to-Year Trends by Need Category")

fig = px.line(
    filtered,
    x="year",
    y="contacts_per_10000",
    color="AIRSNeedCategory",
    line_dash="CityName",
    markers=True,
    labels={
        "contacts_per_10000": "Contacts per 10,000 residents",
        "year": "Year",
        "AIRSNeedCategory": "Need Category"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Needs by Community")

bar_df = (
    filtered.groupby(["CityName", "AIRSNeedCategory"])["contacts_per_10000"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    bar_df,
    x="contacts_per_10000",
    y="AIRSNeedCategory",
    color="CityName",
    orientation="h",
    barmode="group",
    labels={
        "contacts_per_10000": "Contacts per 10,000 residents",
        "AIRSNeedCategory": "Need Category"
    }
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Underlying Data")
st.dataframe(filtered)
