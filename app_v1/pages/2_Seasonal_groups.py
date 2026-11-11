import streamlit as st
import plotly.express as px
from utils import load_data

monthly, seasonal, kpis, monthly_long = load_data()

st.title("🌦️ Seasonal groups")

tab1, tab2, tab3 = st.tabs(["Season patterns", "Most seasonal", "Priority list"])

# Tab 1: average pattern of each season group
with tab1:
    season_shape = (monthly_long.groupby(["peak_season", "month", "month_name"], as_index=False)["index"]
                    .mean())
    fig = px.line(season_shape, x="month_name", y="index", color="peak_season", markers=True,
                  labels={"month_name": "Month", "index": "Seasonality index", "peak_season": "Group"})
    fig.add_hline(y=1, line_dash="dash")
    st.plotly_chart(fig, width="stretch")
    st.write(kpis["peak_season"].value_counts().rename("categories"))

# Tab 2: top seasonal categories
with tab2:
    n = st.slider("Number of categories", 5, 30, 15)
    top = kpis.nlargest(n, "seasonality_score").reset_index()
    fig = px.bar(top, x="seasonality_score", y="category", color="peak_season", orientation="h",
                 hover_data=["peak_month", "low_month", "peak_vs_low"],
                 labels={"seasonality_score": "Seasonality score", "category": ""})
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, width="stretch")

# Tab 3: filterable table
with tab3:
    groups = st.multiselect("Priority group", sorted(kpis["priority"].unique()),
                            default=["1. big & seasonal"])
    table = kpis[kpis["priority"].isin(groups)].sort_values("avg_monthly_clicks", ascending=False)
    st.dataframe(table[["priority", "seasonality_score", "peak_month", "low_month",
                        "avg_monthly_clicks", "peak_season"]])
