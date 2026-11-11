# Page 4: It's all about seasonality - season groups, most seasonal, category deep dive and comparison
import random

import plotly.express as px
import streamlit as st

from ui import (ACCENT, LINE_PALETTE, PRIORITY_COLORS, SEASON_COLORS, SEASON_ICONS, SEASON_ORDER,
                STRENGTH_COLORS, apply_filters, chart_card, chips, empty_state, hero, kpi_cards, style_fig,
                style_lines)
from utils import MONTH_NAMES, load_data

monthly, seasonal, kpis, monthly_long = load_data()
filtered = apply_filters(kpis)

hero("Patterns", "It's all about seasonality",
     "When does each category peak, how strong is its seasonality, and which categories behave alike?")

if filtered.empty:
    empty_state()
    st.stop()

long_f = monthly_long[monthly_long["category"].isin(filtered.index)]

tab1, tab2, tab3, tab4 = st.tabs(["🌦️ Season patterns", "🔥 Most seasonal", "🔍 Category deep dive",
                                  "🔗 Compare & similar"])

# Tab 1: average pattern of each season group
with tab1:
    counts = filtered["peak_season"].value_counts()
    kpi_cards([dict(label=s, count=int(counts.get(s, 0)), icon=SEASON_ICONS[s], color=SEASON_COLORS[s],
                    sub="categories") for s in SEASON_ORDER])

    season_shape = (long_f.groupby(["peak_season", "month", "month_name"], as_index=False)["index"]
                    .mean())
    fig = px.line(season_shape, x="month_name", y="index", color="peak_season", markers=True,
                  color_discrete_map=SEASON_COLORS,
                  category_orders={"peak_season": SEASON_ORDER, "month_name": list(MONTH_NAMES.values())},
                  labels={"month_name": "Month", "index": "Seasonality index", "peak_season": "Group"})
    fig.add_hline(y=1, line_dash="dash", line_color="#94a3b8", annotation_text="average month")
    style_lines(style_fig(fig, height=470, unified=True))
    chart_card(fig, "line", "seasons", "Average pattern per season group",
               "Each line is the mean seasonality index of all categories peaking in that season.")

# Tab 2: top seasonal categories
with tab2:
    max_n = min(30, len(filtered))
    n = st.slider("Number of categories", 1, max_n, min(15, max_n)) if max_n > 1 else max_n
    top = filtered.nlargest(n, "seasonality_score").reset_index()
    top["peak_month"] = top["peak_month"].map(MONTH_NAMES)
    top["low_month"] = top["low_month"].map(MONTH_NAMES)
    fig = px.bar(top, x="seasonality_score", y="category", color="peak_season", orientation="h",
                 hover_data=["peak_month", "low_month", "peak_vs_low"],
                 color_discrete_map=SEASON_COLORS, category_orders={"peak_season": SEASON_ORDER},
                 labels={"seasonality_score": "Seasonality score", "category": "", "peak_season": "Season",
                         "peak_month": "Peak month", "low_month": "Lowest month", "peak_vs_low": "Peak ÷ low"})
    fig.update_yaxes(categoryorder="total ascending")
    style_fig(fig, height=max(380, 30 * n + 120))
    chart_card(fig, "hbar", "top", f"Top {n} most seasonal categories",
               "Seasonality score = highest minus lowest monthly index.")

# Category shared by tab 3 and tab 4 (only categories that pass the sidebar filters)
options = sorted(filtered.index)
if st.session_state.get("category") not in options:
    st.session_state["category"] = "sun care" if "sun care" in options else options[0]


def pick_random():
    choices = [c for c in options if c != st.session_state["category"]] or options
    st.session_state["category"] = random.choice(choices)


# Tab 3: deep dive into one category
with tab3:
    col_sel, col_btn = st.columns([5, 1], vertical_alignment="bottom")
    category = col_sel.selectbox(f"Select a category ({len(options)} available)", options, key="category")
    col_btn.button("🎲 Surprise me", on_click=pick_random, width="stretch")

    row = kpis.loc[category]
    chips([
        (f"{row['strength'].capitalize()} seasonality", STRENGTH_COLORS[row["strength"]]),
        (f"{SEASON_ICONS[row['peak_season']]} {row['peak_season'].capitalize()}", SEASON_COLORS[row["peak_season"]]),
        (f"Priority {row['priority']}", PRIORITY_COLORS[row["priority"]]),
    ])
    kpi_cards([
        dict(label="Seasonality", value=f"{row['seasonality_score']:.2f}", icon="🌡️",
             color=STRENGTH_COLORS[row["strength"]], sub=f"<b>{row['strength']}</b> · max − min index"),
        dict(label="Peak month", value=MONTH_NAMES[row["peak_month"]], icon="⛰️", color="#22c55e",
             sub=f"<b>{row['peak_vs_low']:.1f}×</b> the lowest month"),
        dict(label="Lowest month", value=MONTH_NAMES[row["low_month"]], icon="🕳️", color="#3b82f6",
             sub="weakest month of the year"),
        dict(label="Avg. monthly clicks", value=f"{row['avg_monthly_clicks']:,.0f}", icon="🖱️", color=ACCENT,
             sub=f"rank <b>#{int(kpis['avg_monthly_clicks'].rank(ascending=False)[category])}</b> of {len(kpis)}"),
    ])
    if row["filled_values"] > 0:
        st.info(f"{row['filled_values']} missing month(s) were estimated from the neighbouring months.", icon="ℹ️")

    metric = st.segmented_control("Show", ["clicks", "index"], default="clicks", key="metric",
                                  format_func=lambda x: "Clicks" if x == "clicks"
                                  else "Seasonality index (1 = average)") or "clicks"
    data = monthly_long[monthly_long["category"] == category]
    fig = px.line(data, x="month_name", y=metric, markers=True,
                  labels={"month_name": "Month", metric: metric.capitalize()})
    fig.update_traces(line_color=ACCENT, fill="tozeroy" if metric == "clicks" else None,
                      fillcolor="rgba(99,102,241,0.08)")
    for m, label, color in [(row["peak_month"], "Peak", "#22c55e"), (row["low_month"], "Low", "#3b82f6")]:
        point = data[data["month"] == m].iloc[0]
        fig.add_annotation(x=point["month_name"], y=point[metric], text=f"<b>{label}</b>", showarrow=True,
                           arrowhead=0, ay=-34 if label == "Peak" else 34, bgcolor=color,
                           font=dict(color="white", size=11), bordercolor=color, borderpad=4)
    if metric == "index":
        fig.add_hline(y=1, line_dash="dash", line_color="#94a3b8", annotation_text="average")
    style_lines(style_fig(fig, height=430, unified=True, legend=False))
    chart_card(fig, "line", f"single_{metric}", f"Monthly pattern · {category}")

# Tab 4: compare with other categories
with tab4:
    category = st.session_state["category"]
    st.caption(f"Comparing **{category}**. Change the category in the *Category deep dive* tab.")
    # Most similar categories by monthly pattern
    similar = seasonal.T.corr()[category].drop(category).nlargest(4).index.tolist()
    others = st.multiselect("Compare with", [c for c in sorted(kpis.index) if c != category], default=similar)

    fig = px.line(monthly_long[monthly_long["category"].isin([category] + others)],
                  x="month_name", y="index", color="category", markers=True,
                  category_orders={"category": [category] + others},
                  color_discrete_sequence=LINE_PALETTE,
                  labels={"month_name": "Month", "index": "Seasonality index"})
    fig.add_hline(y=1, line_dash="dash", line_color="#94a3b8")
    style_lines(style_fig(fig, height=460, unified=True))
    fig.update_traces(line_width=2, opacity=0.75)
    fig.update_traces(selector=dict(name=category), line_width=4.5, opacity=1)
    chart_card(fig, "line", "compare", f"{category} vs. similar categories",
               "Default selection = the 4 categories with the most similar pattern. Click a legend item to hide it.")
