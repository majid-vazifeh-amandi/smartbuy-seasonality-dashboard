# Main page: what the web app is and a summary of the project
import streamlit as st

from ui import SEASON_COLORS, hero, kpi_cards, section
from utils import MONTH_NAMES, load_data

monthly, seasonal, kpis, monthly_long = load_data()

hero("Project summary · Content Department",
     "smartbuy: Category Seasonality",
     "A live web app that replaces eyeballing charts: it measures how seasonal each of smartbuy's "
     "100 product categories is, when it peaks, and which categories to plan campaigns for first.",
     chips=["🗂️ 100 categories", "📆 Jan – Dec 2021", "🖱️ Monthly clicks", "⚡ Built with Streamlit & Plotly"])

# ---------------------------------------------------------------- dataset at a glance
total_clicks = monthly.values.sum()
n_strong = int((kpis["strength"] == "strong").sum())
kpi_cards([
    dict(label="Categories", count=len(kpis), icon="🗂️", color="#6366f1", sub="one CSV file each"),
    dict(label="Months", count=12, icon="📆", color="#14b8a6", sub="January to December 2021"),
    dict(label="Total clicks", value=f"{total_clicks / 1e6:.1f} M", icon="🖱️", color="#f59e0b",
         sub="across all categories"),
    dict(label="Strongly seasonal", count=n_strong, icon="🔥", color="#ef4444",
         sub=f"<b>{n_strong / len(kpis):.0%}</b> of all categories"),
])

# ---------------------------------------------------------------- the project
col1, col2 = st.columns(2, gap="medium")
col1.markdown(
    '<div class="text-card"><h3>🎯 The challenge</h3>'
    "<p>smartbuy's Content Department manages the shop's product categories. Until now they judged the "
    "seasonality of a category <b>manually, by eyeballing charts</b>: slow, subjective and hard to repeat.</p>"
    "<p>We received the monthly click data of <b>100 categories</b> (one CSV file per category) and were asked "
    "for a faster, more reliable way to see which categories are seasonal and when they peak.</p></div>",
    unsafe_allow_html=True)
col2.markdown(
    '<div class="text-card"><h3>💡 The solution</h3>'
    "<p>A data pipeline and this <b>interactive web app</b>, so the team can explore the results themselves "
    "instead of waiting for a slide deck.</p><ul>"
    "<li>a <b>seasonality score</b> for every category</li>"
    "<li><b>peak and lowest month</b> and the peak ÷ low ratio</li>"
    "<li><b>priority groups</b> that combine size and seasonality</li>"
    "<li>filters, rankings and comparisons, all in one place</li></ul></div>",
    unsafe_allow_html=True)

st.write("")
section("How we did it", "From 100 raw files to one interactive app")
steps = [
    ("Combine", "Read the 100 CSV files and stack them into one table: 1,200 rows (100 categories × 12 months)."),
    ("Clean", "Check duplicates and fill missing months from the neighbouring months (Dec and Jan count as neighbours)."),
    ("Measure", "Seasonality index = month ÷ category average. Score = highest minus lowest index."),
    ("Prioritise", "Split at the median size and median score into 4 priority groups."),
    ("Share", "Publish everything as this Streamlit app with interactive Plotly charts."),
]
st.markdown('<div class="steps">' + "".join(
    f'<div class="step" style="--d:{i * 0.08:.2f}s"><div class="step-num">{i + 1}</div>'
    f'<b>{title}</b><p>{text}</p></div>' for i, (title, text) in enumerate(steps)) + "</div>",
    unsafe_allow_html=True)

# ---------------------------------------------------------------- key findings (calculated from the data)
month_share = monthly.sum() / monthly.sum().sum() * 100
peak_counts = kpis["peak_month"].value_counts()
season_counts = kpis["peak_season"].value_counts()
top = kpis["seasonality_score"].idxmax()
top_row = kpis.loc[top]
n_focus = int((kpis["priority"] == "1. big & seasonal").sum())
h2_peaks = int(kpis.loc[kpis["strength"] != "flat", "peak_month"].between(9, 12).sum())

findings = [
    ("📈", "#14b8a6",
     f"<b>{MONTH_NAMES[month_share.idxmax()]}</b> is the busiest month with <b>{month_share.max():.1f}%</b> of all "
     f"clicks, <b>{MONTH_NAMES[month_share.idxmin()]}</b> the quietest with <b>{month_share.min():.1f}%</b>."),
    ("🎯", "#f59e0b",
     f"<b>{MONTH_NAMES[peak_counts.idxmax()]}</b> is the most common peak month: "
     f"<b>{peak_counts.max()}</b> categories peak there. {h2_peaks} seasonal categories peak between Sep and Dec."),
    ("❄️", SEASON_COLORS["winter"],
     f"Winter (<b>{season_counts.get('winter', 0)}</b>) and autumn (<b>{season_counts.get('autumn', 0)}</b>) "
     f"peakers clearly outnumber spring (<b>{season_counts.get('spring', 0)}</b>) and summer "
     f"(<b>{season_counts.get('summer', 0)}</b>); <b>{season_counts.get('no clear season', 0)}</b> have no clear season."),
    ("🔥", "#ef4444",
     f"Most seasonal: <b>{top}</b> (score {top_row['seasonality_score']:.2f}), peaking in "
     f"<b>{MONTH_NAMES[top_row['peak_month']]}</b> with <b>{top_row['peak_vs_low']:.1f}×</b> the clicks of its lowest month."),
    ("⭐", "#6366f1",
     f"<b>{n_focus}</b> categories are <b>big & seasonal</b>: plan campaigns, stock and content for these first, "
     f"a few weeks before their peak month."),
]
col1, col2 = st.columns([3, 2], gap="medium")
with col1:
    st.markdown(
        '<div class="text-card"><h3>🔑 Key findings</h3>' + "".join(
            f'<div class="finding" style="--c:{color};--d:{i * 0.1:.1f}s"><div class="ico">{icon}</div><p>{text}</p></div>'
            for i, (icon, color, text) in enumerate(findings)) + "</div>",
        unsafe_allow_html=True)
with col2:
    st.markdown(
        '<div class="text-card"><h3>✅ Recommendations</h3><ul>'
        "<li><b>Replace eyeballing</b> with the seasonality score: anything above 1.0 is strongly seasonal.</li>"
        "<li><b>Start campaigns 4–6 weeks before</b> a category's peak month.</li>"
        "<li><b>Focus on the big & seasonal group</b> first; it has the biggest upside.</li>"
        "<li>Use <b>flat categories</b> as steady, all-year traffic drivers.</li>"
        "<li><b>Refresh the app</b> with each new year of data to track changes.</li></ul></div>",
        unsafe_allow_html=True)

# ---------------------------------------------------------------- navigation cards
st.write("")
section("Explore the app", "Every page has filters in the sidebar")
cards = [
    ("kpis", "📊", "KPIs", "Headline numbers, busiest months and the size vs. seasonality matrix with priority list.",
     "views/kpis.py"),
    ("top", "🏆", "Top clicks", "Rank the categories by clicks and choose how many to show with a slider.",
     "views/top_clicks.py"),
    ("season", "🌦️", "It's all about seasonality", "Season patterns, the most seasonal categories, a deep dive "
     "per category and comparisons.", "views/seasonality.py"),
]
for col, (key, icon, title, text, target) in zip(st.columns(3, gap="medium"), cards):
    with col, st.container(key=f"nav_{key}"):
        st.markdown(f'<div class="nav-icon">{icon}</div><div class="nav-title">{title}</div>'
                    f'<div class="nav-text">{text}</div>', unsafe_allow_html=True)
        st.page_link(target, label=f"Open {title} →", width="stretch")
