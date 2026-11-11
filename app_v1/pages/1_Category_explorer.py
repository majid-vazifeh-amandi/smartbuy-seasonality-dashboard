import streamlit as st
import plotly.express as px
from utils import load_data, MONTH_NAMES

monthly, seasonal, kpis, monthly_long = load_data()

st.title("🔍 Category explorer")

# The user selects a category in the sidebar
category = st.sidebar.selectbox("Select a category", sorted(kpis.index),
                                index=sorted(kpis.index).index("sun care"))
row = kpis.loc[category]

# KPI cards for the selected category
col1, col2, col3, col4 = st.columns(4)
col1.metric("Seasonality", f"{row['seasonality_score']:.2f}", row["strength"], delta_color="off")
col2.metric("Peak month", MONTH_NAMES[row["peak_month"]])
col3.metric("Lowest month", MONTH_NAMES[row["low_month"]])
col4.metric("Avg. monthly clicks", f"{row['avg_monthly_clicks']:,.0f}")

if row["filled_values"] > 0:
    st.info(f"{row['filled_values']} missing month(s) were estimated from the neighbouring months.")

tab1, tab2 = st.tabs(["📈 Monthly clicks", "🔗 Compare & similar"])

# Tab 1: monthly pattern of the selected category
with tab1:
    metric = st.radio("Show", ["clicks", "index"], horizontal=True,
                      format_func=lambda x: "Clicks" if x == "clicks" else "Seasonality index (1 = average)")
    fig = px.line(monthly_long[monthly_long["category"] == category],
                  x="month_name", y=metric, markers=True,
                  labels={"month_name": "Month", metric: metric.capitalize()})
    st.plotly_chart(fig, width="stretch")

# Tab 2: compare with other categories
with tab2:
    # Most similar categories by monthly pattern
    similar = seasonal.T.corr()[category].drop(category).nlargest(4).index.tolist()
    others = st.multiselect("Compare with", sorted(kpis.index), default=similar)

    fig = px.line(monthly_long[monthly_long["category"].isin([category] + others)],
                  x="month_name", y="index", color="category", markers=True,
                  labels={"month_name": "Month", "index": "Seasonality index"})
    st.plotly_chart(fig, width="stretch")
    st.caption("Default selection = the 4 categories with the most similar pattern.")
