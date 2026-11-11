# Shared data loading and KPI calculations (same logic as the Day 2 notebook)
import pandas as pd
import numpy as np
import streamlit as st

MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

SEASON_MAP = {12: "winter", 1: "winter", 2: "winter",
              3: "spring", 4: "spring", 5: "spring",
              6: "summer", 7: "summer", 8: "summer",
              9: "autumn", 10: "autumn", 11: "autumn"}


def fill_circular(row):
    # Fill missing months; January and December are treated as neighbours
    tripled = pd.concat([row, row, row], ignore_index=True)
    filled = tripled.interpolate()
    return pd.Series(filled.iloc[12:24].values, index=row.index)


@st.cache_data  # calculate once, not on every click
def load_data():
    df = pd.read_csv("data/combined_categories.csv")

    # Wide table: one row per category, one column per month
    monthly_raw = df.pivot(index="category", columns="month", values="clicks")
    monthly = monthly_raw.apply(fill_circular, axis=1)
    seasonal = monthly.div(monthly.mean(axis=1), axis=0)

    # KPIs per category
    kpis = pd.DataFrame({
        "seasonality_score": seasonal.max(axis=1) - seasonal.min(axis=1),
        "peak_month": seasonal.idxmax(axis=1),
        "low_month": seasonal.idxmin(axis=1),
        "avg_monthly_clicks": monthly.mean(axis=1),
        "peak_vs_low": monthly.max(axis=1) / monthly.min(axis=1),
        "filled_values": monthly_raw.isna().sum(axis=1),
    }).round(2)

    kpis["strength"] = pd.cut(kpis["seasonality_score"], bins=[0, 0.5, 1.0, np.inf],
                              labels=["flat", "moderate", "strong"]).astype(str)
    kpis["peak_season"] = kpis["peak_month"].map(SEASON_MAP)
    kpis.loc[kpis["strength"] == "flat", "peak_season"] = "no clear season"

    # Priority groups: split at the median size and median score
    is_big = kpis["avg_monthly_clicks"] >= kpis["avg_monthly_clicks"].median()
    is_seasonal = kpis["seasonality_score"] >= kpis["seasonality_score"].median()
    kpis["priority"] = np.select(
        [is_big & is_seasonal, ~is_big & is_seasonal, is_big & ~is_seasonal],
        ["1. big & seasonal", "2. small & seasonal", "3. big & steady"],
        default="4. small & steady",
    )

    # Long table for charts: one row per category and month
    monthly_long = (monthly.stack().rename("clicks").to_frame()
                    .join(seasonal.stack().rename("index"))
                    .reset_index())
    monthly_long["month_name"] = monthly_long["month"].map(MONTH_NAMES)
    monthly_long = monthly_long.merge(kpis[["peak_season", "strength", "priority"]],
                                      left_on="category", right_index=True)

    return monthly, seasonal, kpis, monthly_long
