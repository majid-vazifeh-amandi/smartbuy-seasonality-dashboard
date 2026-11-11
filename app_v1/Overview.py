import streamlit as st
import plotly.express as px
from utils import load_data, MONTH_NAMES

st.set_page_config(page_title="smartbuy Seasonality", page_icon="📅", layout="wide")

monthly, seasonal, kpis, monthly_long = load_data()

# Sidebar
st.sidebar.markdown("# smartbuy Seasonality")
st.sidebar.markdown("Monthly clicks of 100 categories (2021).")

# Title
st.title("📅 smartbuy: Category Seasonality")
st.write("""
Which categories are seasonal, and when do they peak?
Use the pages in the sidebar to explore single categories and seasonal groups.
""")

# KPI cards: the most important numbers first
month_share = monthly.sum() / monthly.sum().sum() * 100
busiest_month = month_share.idxmax()
top_peak_month = kpis["peak_month"].value_counts().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Categories", len(kpis))
col2.metric("Strongly seasonal", (kpis["strength"] == "strong").sum())
col3.metric("Busiest month", MONTH_NAMES[busiest_month], f"{month_share.max():.1f}% of clicks")
col4.metric("Most common peak", MONTH_NAMES[top_peak_month],
            f"{kpis['peak_month'].value_counts().max()} categories")

st.divider()

# Chart 1: share of clicks per month
st.subheader("When is the shop busiest?")
month_plot = month_share.round(1).rename("share").reset_index()
month_plot["month_name"] = month_plot["month"].map(MONTH_NAMES)
month_plot["categories_peaking"] = month_plot["month"].map(kpis["peak_month"].value_counts()).fillna(0)

fig = px.bar(month_plot, x="month_name", y="share", hover_data=["categories_peaking"],
             labels={"month_name": "Month", "share": "Share of clicks (%)"})
fig.add_hline(y=100 / 12, line_dash="dash", annotation_text="average month")
st.plotly_chart(fig, width="stretch")

# Chart 2: size vs seasonality
st.subheader("Which categories matter most?")
st.caption("Top right = big and seasonal: plan campaigns for these first.")
fig = px.scatter(kpis.reset_index(), x="seasonality_score", y="avg_monthly_clicks",
                 color="priority", hover_name="category", hover_data=["peak_month", "low_month"],
                 labels={"seasonality_score": "Seasonality score",
                         "avg_monthly_clicks": "Average monthly clicks"})
fig.add_vline(x=kpis["seasonality_score"].median(), line_dash="dash")
fig.add_hline(y=kpis["avg_monthly_clicks"].median(), line_dash="dash")
st.plotly_chart(fig, width="stretch")

# TODO (Day 3): add key findings and recommendations here
