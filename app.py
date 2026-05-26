import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Community Resilience Dashboard", layout="wide")

st.title("Community Resilience Dashboard")
st.caption("211 community needs data normalized by population")

df = pd.read_csv("city_year_trends.csv")

# Sidebar filters
cities = sorted(df["CityName"].dropna().unique())
categories = sorted(df["AIRSNeedCategory"].dropna().unique())
years = sorted(df["year"].dropna().unique())

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

selected_years = st.sidebar.multiselect(
    "Select years",
    years,
    default=[2024, 2025]
)

filtered = df[
    (df["CityName"].isin(selected_cities)) &
    (df["AIRSNeedCategory"].isin(selected_categories)) &
    (df["year"].isin(selected_years))
]

# Top summary cards
col1, col2, col3 = st.columns(3)

col1.metric("Communities selected", filtered["CityName"].nunique())
col2.metric("Need categories selected", filtered["AIRSNeedCategory"].nunique())
col3.metric("Total contacts", f"{filtered['contact_count'].sum():,.0f}")

#Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Trends",
    "Top Needs",
    "Community Comparison",
    "Top Needs by Year",
    "Data Table"
])
with tab1:
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
            "AIRSNeedCategory": "Need Category",
            "CityName": "Community"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
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
            "AIRSNeedCategory": "Need Category",
            "CityName": "Community"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Community Comparison")

    comparison_df = (
        filtered.groupby(["CityName", "year"])["contacts_per_10000"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        comparison_df,
        x="CityName",
        y="contacts_per_10000",
        color="year",
        barmode="group",
        labels={
            "contacts_per_10000": "Total contacts per 10,000 residents",
            "CityName": "Community",
            "year": "Year"
        }
    )

    st.plotly_chart(fig3, use_container_width=True)
with tab4:
    st.subheader("Top Needs by Year for Each Community")

    top_needs_year = (
        filtered.groupby(["CityName", "year", "AIRSNeedCategory"])["contacts_per_10000"]
        .sum()
        .reset_index()
    )

    top_needs_year["rank"] = (
        top_needs_year
        .groupby(["CityName", "year"])["contacts_per_10000"]
        .rank(method="first", ascending=False)
    )

    top_needs_year = top_needs_year[top_needs_year["rank"] <= 5]

    fig4 = px.bar(
        top_needs_year,
        x="contacts_per_10000",
        y="AIRSNeedCategory",
        color="year",
        facet_col="CityName",
        orientation="h",
        barmode="group",
        labels={
            "contacts_per_10000": "Contacts per 10,000 residents",
            "AIRSNeedCategory": "Need Category",
            "year": "Year",
            "CityName": "Community"
        },
        title="Top 5 Needs by Year for Each Community"
    )

    fig4.update_yaxes(categoryorder="total ascending")
    fig4.update_layout(height=650)

    st.plotly_chart(fig4, use_container_width=True)
with tab5:
    st.subheader("Filtered Data")
    st.dataframe(filtered, use_container_width=True)
