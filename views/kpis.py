# Page 2: KPIs - headline numbers, clicks per month, size vs. seasonality and the priority list
import plotly.express as px
import streamlit as st

from ui import (ACCENT, PRIORITY_COLORS, SEASON_ICONS, apply_filters, chart_card, empty_state, hero,
                kpi_cards, section, style_fig)
from utils import MONTH_NAMES, load_data

monthly, seasonal, kpis, monthly_long = load_data()
filtered = apply_filters(kpis)

hero("Key performance indicators", "KPIs",
     "The most important numbers first, then when the shop is busiest and which categories matter most.")

if filtered.empty:
    empty_state()
    st.stop()

# KPI cards (for the current filter selection)
sel = monthly.loc[filtered.index]
month_share = sel.sum() / sel.sum().sum() * 100
busiest_month = month_share.idxmax()
peak_counts = filtered["peak_month"].value_counts()
n_strong = int((filtered["strength"] == "strong").sum())

kpi_cards([
    dict(label="Categories", count=len(filtered), icon="🗂️", color="#6366f1",
         sub=f"<b>{len(filtered) / len(kpis):.0%}</b> of all {len(kpis)}"),
    dict(label="Strongly seasonal", count=n_strong, icon="🔥", color="#ef4444",
         sub=f"<b>{n_strong / len(filtered):.0%}</b> of the selection"),
    dict(label="Busiest month", value=MONTH_NAMES[busiest_month], icon="📈", color="#14b8a6",
         sub=f"<b>{month_share.max():.1f}%</b> of clicks"),
    dict(label="Most common peak", value=MONTH_NAMES[peak_counts.idxmax()], icon="🎯", color="#f59e0b",
         sub=f"<b>{peak_counts.max()}</b> categories peak here"),
    dict(label="Avg. seasonality", value=f"{filtered['seasonality_score'].mean():.2f}", icon="🌡️",
         color="#8b5cf6", sub=f"median <b>{filtered['seasonality_score'].median():.2f}</b>"),
])

# Chart 1: share of clicks per month
month_plot = month_share.round(1).rename("share").reset_index()
month_plot["month_name"] = month_plot["month"].map(MONTH_NAMES)
month_plot["categories_peaking"] = month_plot["month"].map(peak_counts).fillna(0)

fig = px.bar(month_plot, x="month_name", y="share", hover_data=["categories_peaking"],
             labels={"month_name": "Month", "share": "Share of clicks (%)",
                     "categories_peaking": "Categories peaking"})
fig.update_traces(marker_color=["#f59e0b" if m == busiest_month else "#a5b4fc" for m in month_plot["month"]],
                  hovertemplate="<b>%{x}</b><br>Share of clicks: %{y:.1f}%"
                                "<br>Categories peaking: %{customdata[0]:.0f}<extra></extra>")
fig.add_hline(y=100 / 12, line_dash="dash", line_color=ACCENT, annotation_text="average month",
              annotation_font_color=ACCENT)
style_fig(fig, height=400, legend=False)
chart_card(fig, "bar", "months", "When is the shop busiest?",
           "Share of all clicks per month. The busiest month is highlighted.")

st.write("")

# Chart 2: size vs seasonality
fig = px.scatter(filtered.reset_index(), x="seasonality_score", y="avg_monthly_clicks",
                 color="priority", hover_name="category", hover_data=["peak_month", "low_month"],
                 color_discrete_map=PRIORITY_COLORS,
                 category_orders={"priority": list(PRIORITY_COLORS)},
                 labels={"seasonality_score": "Seasonality score",
                         "avg_monthly_clicks": "Average monthly clicks",
                         "peak_month": "Peak month", "low_month": "Lowest month"})
fig.update_traces(marker=dict(size=13, opacity=0.88, line=dict(width=1.5, color="white")))
# median lines from all categories, because the priority groups are defined on them
fig.add_vline(x=kpis["seasonality_score"].median(), line_dash="dash", line_color="#94a3b8")
fig.add_hline(y=kpis["avg_monthly_clicks"].median(), line_dash="dash", line_color="#94a3b8")
fig.add_annotation(x=1, y=1, xref="x domain", yref="y domain", text="★ focus area", showarrow=False,
                   font=dict(color=ACCENT, size=12), xanchor="right", yanchor="top")
style_fig(fig, height=500)
chart_card(fig, "scatter", "priority", "Which categories matter most?",
           "Top right = big and seasonal: plan campaigns for these first.")

# Priority list
st.write("")
section("Priority list", "All categories of the chosen priority groups")
c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
groups = c1.multiselect("Priority group", list(PRIORITY_COLORS), default=["1. big & seasonal"],
                        placeholder="All groups")
sort_by = c2.selectbox("Sort by", ["avg_monthly_clicks", "seasonality_score", "peak_vs_low"],
                       format_func=lambda c: {"avg_monthly_clicks": "Avg. clicks",
                                              "seasonality_score": "Seasonality",
                                              "peak_vs_low": "Peak ÷ low"}[c])
table = filtered[filtered["priority"].isin(groups)] if groups else filtered
table = table.sort_values(sort_by, ascending=False)[
    ["priority", "seasonality_score", "peak_month", "low_month", "avg_monthly_clicks", "peak_season"]].copy()
table["peak_month"] = table["peak_month"].map(MONTH_NAMES)
table["low_month"] = table["low_month"].map(MONTH_NAMES)
table["peak_season"] = table["peak_season"].map(lambda s: f"{SEASON_ICONS[s]} {s}")
table["avg_monthly_clicks"] = table["avg_monthly_clicks"].round().astype(int)

st.dataframe(
    table, width="stretch", height=min(500, 36 * len(table) + 40),
    column_config={
        "_index": st.column_config.TextColumn("Category"),
        "priority": st.column_config.TextColumn("Priority"),
        "seasonality_score": st.column_config.ProgressColumn(
            "Seasonality", format="%.2f", min_value=0, max_value=float(kpis["seasonality_score"].max())),
        "peak_month": st.column_config.TextColumn("Peak"),
        "low_month": st.column_config.TextColumn("Low"),
        "avg_monthly_clicks": st.column_config.NumberColumn("Avg. clicks", format="localized"),
        "peak_season": st.column_config.TextColumn("Season"),
    },
)
st.download_button("⬇️ Download as CSV", table.to_csv().encode("utf-8"),
                   file_name="smartbuy_priority_list.csv", mime="text/csv")
