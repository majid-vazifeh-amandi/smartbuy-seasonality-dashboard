# Page 3: Top n categories by clicks, n chosen with a slider
import plotly.express as px
import streamlit as st

from ui import (SEASON_COLORS, SEASON_ICONS, SEASON_ORDER, apply_filters, chart_card, empty_state, hero,
                kpi_cards, style_fig)
from utils import MONTH_NAMES, load_data

monthly, seasonal, kpis, monthly_long = load_data()
filtered = apply_filters(kpis)

hero("Ranking", "Top clicks",
     "Which categories attract the most clicks? Choose how many to show with the slider.")

if filtered.empty:
    empty_state()
    st.stop()

# Ranking table: total clicks over the year per category
ranking = filtered.copy()
ranking["total_clicks"] = monthly.loc[filtered.index].sum(axis=1)
ranking = ranking.sort_values("total_clicks", ascending=False)

max_n = len(ranking)
if max_n > 1:
    n = st.slider("🏆 Number of top categories (n)", 1, max_n, min(10, max_n), key="top_n")
else:
    n = max_n
top = ranking.head(n)

top_share = top["total_clicks"].sum() / monthly.values.sum() * 100
leader = top.index[0]
kpi_cards([
    dict(label="Top n", count=n, icon="🏆", color="#6366f1", sub=f"of {max_n} categories in the selection"),
    dict(label="#1 category", value=leader, icon="🥇", color="#f59e0b",
         sub=f"<b>{top['total_clicks'].iloc[0]:,.0f}</b> clicks in 2021"),
    dict(label="Clicks of the top n", value=f"{top['total_clicks'].sum() / 1e6:.2f} M", icon="🖱️", color="#14b8a6",
         sub=f"<b>{top_share:.1f}%</b> of all smartbuy clicks"),
    dict(label="Seasonal in the top n", count=int((top["strength"] != "flat").sum()), icon="🔥", color="#ef4444",
         sub="moderate or strong seasonality"),
])

# Bar chart: top n by total clicks
plot = top.reset_index()
plot["peak_month"] = plot["peak_month"].map(MONTH_NAMES)
plot["rank"] = range(1, len(plot) + 1)
fig = px.bar(plot, x="total_clicks", y="category", color="peak_season", orientation="h",
             hover_data={"rank": True, "avg_monthly_clicks": ":,.0f", "peak_month": True,
                         "seasonality_score": ":.2f", "total_clicks": ":,.0f"},
             color_discrete_map=SEASON_COLORS, category_orders={"peak_season": SEASON_ORDER},
             text="total_clicks",
             labels={"total_clicks": "Total clicks 2021", "category": "", "peak_season": "Peak season",
                     "avg_monthly_clicks": "Avg. monthly clicks", "peak_month": "Peak month",
                     "seasonality_score": "Seasonality", "rank": "Rank"})
fig.update_traces(texttemplate="%{x:,.0f}", textposition="inside", insidetextanchor="end",
                  textfont=dict(color="white", size=11))
fig.update_yaxes(categoryorder="total ascending")
style_fig(fig, height=max(360, 32 * n + 130))
chart_card(fig, "hbar", "topclicks", f"Top {n} categories by clicks",
           "Total clicks over all 12 months of 2021. Colour = season in which the category peaks.")

# Table of the top n
st.write("")
table = top[["total_clicks", "avg_monthly_clicks", "peak_month", "peak_season", "seasonality_score"]].copy()
table.insert(0, "rank", range(1, len(table) + 1))
table["total_clicks"] = table["total_clicks"].round().astype(int)
table["avg_monthly_clicks"] = table["avg_monthly_clicks"].round().astype(int)
table["peak_month"] = table["peak_month"].map(MONTH_NAMES)
table["peak_season"] = table["peak_season"].map(lambda s: f"{SEASON_ICONS[s]} {s}")
st.dataframe(
    table, width="stretch", height=min(500, 36 * len(table) + 40),
    column_config={
        "_index": st.column_config.TextColumn("Category"),
        "rank": st.column_config.NumberColumn("Rank", format="#%d"),
        "total_clicks": st.column_config.ProgressColumn(
            "Total clicks", format="localized", min_value=0, max_value=float(ranking["total_clicks"].max())),
        "avg_monthly_clicks": st.column_config.NumberColumn("Avg. / month", format="localized"),
        "peak_month": st.column_config.TextColumn("Peak"),
        "peak_season": st.column_config.TextColumn("Season"),
        "seasonality_score": st.column_config.NumberColumn("Seasonality", format="%.2f"),
    },
)
st.download_button("⬇️ Download top list as CSV", table.to_csv().encode("utf-8"),
                   file_name=f"smartbuy_top_{n}_clicks.csv", mime="text/csv")
