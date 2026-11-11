# Look & feel for the smartbuy app: theme CSS, animations, KPI cards,
# chart styling and the shared sidebar filters used on every page.
import html

import streamlit as st

from utils import MONTH_NAMES

# ---------------------------------------------------------------- colours
ACCENT = "#6366f1"
TEXT = "#1e293b"
MUTED = "#64748b"

SEASON_ORDER = ["winter", "spring", "summer", "autumn", "no clear season"]
SEASON_COLORS = {"winter": "#3b82f6", "spring": "#22c55e", "summer": "#f59e0b",
                 "autumn": "#ea580c", "no clear season": "#94a3b8"}
SEASON_ICONS = {"winter": "❄️", "spring": "🌱", "summer": "☀️",
                "autumn": "🍂", "no clear season": "➖"}

PRIORITY_COLORS = {"1. big & seasonal": "#6366f1", "2. small & seasonal": "#a78bfa",
                   "3. big & steady": "#14b8a6", "4. small & steady": "#cbd5e1"}

STRENGTH_COLORS = {"strong": "#ef4444", "moderate": "#f59e0b", "flat": "#94a3b8"}

LINE_PALETTE = ["#6366f1", "#ec4899", "#14b8a6", "#f59e0b", "#3b82f6",
                "#8b5cf6", "#ef4444", "#22c55e", "#0ea5e9", "#f97316"]

MONTH_LIST = list(MONTH_NAMES.values())
MONTH_NUM = {name: num for num, name in MONTH_NAMES.items()}

# ---------------------------------------------------------------- CSS
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp li,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stMarkdown, .stButton button,
[data-testid="stMetricValue"], .stTabs button p { font-family: 'Inter', sans-serif; }

.stApp {
  background:
    radial-gradient(1200px 500px at 100% -10%, rgba(99,102,241,.10), transparent 60%),
    radial-gradient(900px 400px at -10% 110%, rgba(236,72,153,.07), transparent 60%),
    #f5f7fb;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 1300px; }

/* ---------- keyframes ---------- */
@keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes float { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(-30px,20px) scale(1.12); } }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,.7); } 70% { box-shadow: 0 0 0 10px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }
@keyframes wipeX { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes wipeUp { from { clip-path: inset(100% 0 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes countUp { to { --num: var(--target); } }
@keyframes shimmer { from { background-position: -200% 0; } to { background-position: 200% 0; } }

@property --num { syntax: '<integer>'; initial-value: 0; inherits: false; }

/* ---------- hero banner ---------- */
.hero {
  position: relative; overflow: hidden; border-radius: 22px; padding: 30px 34px; margin-bottom: 1.4rem;
  color: #fff; background: linear-gradient(120deg, #4f46e5, #7c3aed, #db2777, #f59e0b, #4f46e5);
  background-size: 300% 300%; animation: gradientShift 14s ease infinite, fadeUp .7s ease both;
  box-shadow: 0 20px 45px -18px rgba(79,70,229,.55);
}
.hero::before, .hero::after {
  content: ""; position: absolute; border-radius: 50%; filter: blur(2px);
  background: rgba(255,255,255,.14); animation: float 9s ease-in-out infinite;
}
.hero::before { width: 260px; height: 260px; right: -60px; top: -90px; }
.hero::after  { width: 160px; height: 160px; right: 180px; bottom: -80px; animation-delay: -4s; }
.hero-eyebrow { display: inline-flex; align-items: center; gap: 8px; font-size: .78rem; font-weight: 600;
  letter-spacing: .08em; text-transform: uppercase; opacity: .92; }
.hero-dot { width: 8px; height: 8px; border-radius: 50%; background: #fff; animation: pulse 2s infinite; }
.hero h1 { color: #fff !important; font-size: 2.3rem !important; font-weight: 800 !important;
  margin: .35rem 0 .3rem 0 !important; padding: 0 !important; letter-spacing: -.02em; }
.hero p { color: rgba(255,255,255,.9) !important; font-size: 1.05rem; max-width: 760px; margin: 0; }
.hero-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; position: relative; z-index: 1; }
.hero-chip { background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.28); backdrop-filter: blur(6px);
  padding: 5px 12px; border-radius: 999px; font-size: .82rem; font-weight: 500; }

/* ---------- KPI cards ---------- */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(165px, 1fr)); gap: 16px; margin: .4rem 0 1.4rem; }
.kpi {
  position: relative; overflow: hidden; background: #fff; border: 1px solid #e8ebf3; border-radius: 18px;
  padding: 18px 20px 16px; box-shadow: 0 1px 2px rgba(15,23,42,.04), 0 10px 28px -12px rgba(15,23,42,.12);
  transition: transform .25s ease, box-shadow .25s ease; animation: fadeUp .6s ease both; animation-delay: var(--d);
}
.kpi::before { content: ""; position: absolute; inset: 0 0 auto 0; height: 4px; background: var(--c, #6366f1); }
.kpi:hover { transform: translateY(-5px); box-shadow: 0 2px 4px rgba(15,23,42,.05), 0 22px 40px -16px rgba(79,70,229,.35); }
.kpi-top { display: flex; justify-content: space-between; align-items: center; }
.kpi-label { font-size: .76rem; font-weight: 600; text-transform: uppercase; letter-spacing: .07em; color: #64748b; }
.kpi-icon { width: 36px; height: 36px; display: grid; place-items: center; border-radius: 11px; font-size: 1.1rem;
  background: color-mix(in srgb, var(--c, #6366f1) 14%, white); }
.kpi-value { font-size: 2rem; font-weight: 800; color: #0f172a; margin-top: 6px; letter-spacing: -.02em; line-height: 1.15;
  overflow-wrap: anywhere; }
.kpi-sub { margin-top: 6px; font-size: .84rem; color: #64748b; }
.kpi-sub b { color: var(--c, #6366f1); }
.count { animation: countUp 1.4s cubic-bezier(.2,.8,.2,1) forwards; counter-reset: num var(--num); }
.count::after { content: counter(num); }

/* ---------- chips / badges ---------- */
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin: .2rem 0 1rem; animation: fadeIn .6s ease both; }
.chip { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 999px; font-size: .82rem;
  font-weight: 600; color: var(--c); background: color-mix(in srgb, var(--c) 12%, white);
  border: 1px solid color-mix(in srgb, var(--c) 30%, white); }

/* ---------- section titles ---------- */
.section { margin: .2rem 0 .2rem; animation: fadeUp .6s ease both; }
.section h3 { font-size: 1.15rem !important; font-weight: 700 !important; color: #0f172a; margin: 0 !important; padding: 0 !important; }
.section p { color: #64748b; font-size: .88rem; margin: .15rem 0 0; }

/* ---------- chart cards ---------- */
[class*="st-key-card_"] {
  background: #fff; border: 1px solid #e8ebf3; border-radius: 20px; padding: 18px 20px 8px;
  box-shadow: 0 1px 2px rgba(15,23,42,.04), 0 12px 32px -16px rgba(15,23,42,.14);
  animation: fadeUp .7s ease both; transition: box-shadow .3s ease, transform .3s ease;
}
[class*="st-key-card_"]:hover { box-shadow: 0 2px 4px rgba(15,23,42,.05), 0 24px 44px -20px rgba(79,70,229,.30); }
[class*="st-key-card_line"] .scatterlayer { animation: wipeX 1.6s cubic-bezier(.4,0,.2,1) both; }
[class*="st-key-card_bar"] .barlayer { animation: wipeUp 1.1s cubic-bezier(.4,0,.2,1) both; }
[class*="st-key-card_hbar"] .barlayer { animation: wipeX 1.2s cubic-bezier(.4,0,.2,1) both; }
[class*="st-key-card_scatter"] .scatterlayer .point { animation: fadeIn .9s ease both; }
[class*="st-key-card_scatter"] .scatterlayer .point:nth-child(3n+1) { animation-delay: .15s; }
[class*="st-key-card_scatter"] .scatterlayer .point:nth-child(3n+2) { animation-delay: .35s; }
[class*="st-key-card_scatter"] .scatterlayer .point:nth-child(3n)   { animation-delay: .55s; }

/* ---------- tabs ---------- */
.stTabs [role="tablist"] { gap: 6px; background: #fff; padding: 6px; border-radius: 14px; border: 1px solid #e8ebf3 !important;
  box-shadow: 0 6px 18px -12px rgba(15,23,42,.15); width: fit-content; max-width: 100%; overflow-x: auto; }
.stTabs [role="tablist"]::before, .stTabs [role="tablist"]::after { display: none !important; }
.stTabs [role="tab"] { border-radius: 10px !important; padding: 8px 18px !important; height: auto !important; margin: 0 !important;
  white-space: nowrap; transition: background .2s ease, box-shadow .2s ease; border: none !important; }
.stTabs [role="tab"]:hover { background: #f1f2fb; }
.stTabs [role="tab"][aria-selected="true"] { background: linear-gradient(120deg, #6366f1, #8b5cf6) !important;
  box-shadow: 0 8px 18px -8px rgba(99,102,241,.7); }
.stTabs [role="tab"][aria-selected="true"] p { color: #fff !important; }
.stTabs .react-aria-SelectionIndicator, .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [role="tablist"] + div, .stTabs [role="tablist"] ~ * { border: none; }
.stTabs [role="tabpanel"] { animation: fadeIn .45s ease both; padding-top: .6rem; }

/* ---------- buttons ---------- */
.stButton button, .stDownloadButton button { border-radius: 12px; font-weight: 600; transition: all .2s ease; }
.stButton button:hover, .stDownloadButton button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px -10px rgba(99,102,241,.6); }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #ffffff 0%, #f6f5ff 100%); border-right: 1px solid #e8ebf3; }
.sb-brand { display: flex; align-items: center; gap: 12px; padding: 4px 0 14px; border-bottom: 1px solid #ebeaf7; margin-bottom: 14px; }
.sb-logo { width: 42px; height: 42px; border-radius: 13px; display: grid; place-items: center; font-size: 1.3rem;
  background: linear-gradient(135deg, #6366f1, #db2777); box-shadow: 0 8px 18px -8px rgba(99,102,241,.8); }
.sb-name { font-weight: 800; color: #0f172a; font-size: 1.05rem; line-height: 1.1; }
.sb-tag { color: #64748b; font-size: .78rem; }
.sb-title { font-size: .74rem; font-weight: 700; text-transform: uppercase; letter-spacing: .09em; color: #6366f1; margin: 4px 0 2px; }
.sb-count { background: #fff; border: 1px solid #e8ebf3; border-radius: 14px; padding: 12px 14px; margin: 10px 0; font-size: .85rem; color: #64748b; }
.sb-count b { font-size: 1.35rem; color: #0f172a; font-weight: 800; }
.sb-bar { height: 7px; background: #eef0f7; border-radius: 99px; margin-top: 8px; overflow: hidden; }
.sb-bar div { height: 100%; border-radius: 99px; transition: width .6s cubic-bezier(.2,.8,.2,1);
  background: linear-gradient(90deg, #6366f1, #ec4899, #6366f1); background-size: 200% 100%; animation: shimmer 3s linear infinite; }

/* ---------- empty state ---------- */
.empty { text-align: center; padding: 60px 20px; background: #fff; border: 2px dashed #dfe3ef; border-radius: 20px; animation: fadeUp .5s ease both; }
.empty .big { font-size: 3rem; }
.empty h3 { margin: .4rem 0 .2rem !important; }
.empty p { color: #64748b; }

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; animation: fadeUp .6s ease both; }

/* ---------- home page: text card, steps, findings, nav cards ---------- */
.text-card { background: #fff; border: 1px solid #e8ebf3; border-radius: 20px; padding: 22px 26px; height: 100%;
  box-shadow: 0 12px 32px -18px rgba(15,23,42,.14); animation: fadeUp .7s ease both; }
.text-card h3 { font-size: 1.15rem !important; font-weight: 700 !important; margin: 0 0 .5rem !important; padding: 0 !important; }
.text-card p, .text-card li { color: #475569; font-size: .95rem; line-height: 1.6; }
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; margin: .6rem 0 1.4rem; }
.step { position: relative; background: #fff; border: 1px solid #e8ebf3; border-radius: 18px; padding: 18px;
  animation: fadeUp .6s ease both; animation-delay: var(--d); transition: transform .25s ease, box-shadow .25s ease; }
.step:hover { transform: translateY(-4px); box-shadow: 0 20px 36px -18px rgba(79,70,229,.35); }
.step-num { width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font-weight: 800; color: #fff;
  background: linear-gradient(135deg, #6366f1, #db2777); margin-bottom: 10px; }
.step b { color: #0f172a; }
.step p { color: #64748b; font-size: .86rem; margin: .3rem 0 0; line-height: 1.5; }
.finding { display: flex; gap: 12px; align-items: flex-start; padding: 12px 0; border-bottom: 1px dashed #e2e8f0;
  animation: fadeUp .6s ease both; animation-delay: var(--d); }
.finding:last-child { border-bottom: none; }
.finding .ico { flex: 0 0 34px; height: 34px; border-radius: 10px; display: grid; place-items: center;
  background: color-mix(in srgb, var(--c) 14%, white); }
.finding p { margin: 0; color: #334155; font-size: .93rem; line-height: 1.55; }
[class*="st-key-nav_"] { background: #fff; border: 1px solid #e8ebf3; border-radius: 20px; padding: 20px 20px 12px;
  box-shadow: 0 12px 32px -18px rgba(15,23,42,.14); animation: fadeUp .7s ease both; height: 100%;
  transition: transform .25s ease, box-shadow .25s ease; }
[class*="st-key-nav_"]:hover { transform: translateY(-6px); box-shadow: 0 26px 44px -20px rgba(79,70,229,.4); }
.nav-icon { font-size: 1.8rem; }
.nav-title { font-weight: 800; font-size: 1.1rem; color: #0f172a; margin: 4px 0 2px; }
.nav-text { color: #64748b; font-size: .88rem; line-height: 1.5; min-height: 3.9em; }
[class*="st-key-nav_"] [data-testid="stPageLink-NavLink"] {
  background: linear-gradient(120deg, #6366f1, #8b5cf6) !important; border-radius: 12px !important;
  justify-content: center; padding: 8px 14px !important; transition: transform .2s ease, box-shadow .2s ease; }
[class*="st-key-nav_"] [data-testid="stPageLink-NavLink"]:hover { transform: translateY(-2px);
  box-shadow: 0 10px 20px -10px rgba(99,102,241,.8); }
[class*="st-key-nav_"] [data-testid="stPageLink-NavLink"] p { color: #fff !important; font-weight: 600; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  .count { counter-reset: num var(--target); }
}
</style>
"""


def setup_page(title, icon):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)


def _h(text):
    return html.escape(str(text))


def hero(eyebrow, title, subtitle, chips=()):
    chip_html = "".join(f'<span class="hero-chip">{_h(c)}</span>' for c in chips)
    st.markdown(
        f'<div class="hero"><div class="hero-eyebrow"><span class="hero-dot"></span>{_h(eyebrow)}</div>'
        f'<h1>{_h(title)}</h1><p>{_h(subtitle)}</p><div class="hero-chips">{chip_html}</div></div>',
        unsafe_allow_html=True,
    )


def kpi_cards(cards):
    """cards: list of dicts with label, icon, sub and either count (int, animated) or value (text)."""
    parts = []
    for i, c in enumerate(cards):
        if c.get("count") is not None:
            value = f'<span class="count" style="--target:{int(c["count"])}" aria-label="{int(c["count"])}"></span>'
        else:
            value = _h(c["value"])
        parts.append(
            f'<div class="kpi" style="--d:{i * 0.09:.2f}s;--c:{c.get("color", ACCENT)}">'
            f'<div class="kpi-top"><span class="kpi-label">{_h(c["label"])}</span>'
            f'<span class="kpi-icon">{c.get("icon", "")}</span></div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-sub">{c.get("sub", "")}</div></div>'
        )
    st.markdown(f'<div class="kpi-grid">{"".join(parts)}</div>', unsafe_allow_html=True)


def chips(items):
    """items: list of (text, colour)."""
    st.markdown('<div class="chips">' + "".join(
        f'<span class="chip" style="--c:{color}">{_h(text)}</span>' for text, color in items) + "</div>",
        unsafe_allow_html=True)


def section(title, caption=""):
    cap = f"<p>{_h(caption)}</p>" if caption else ""
    st.markdown(f'<div class="section"><h3>{_h(title)}</h3>{cap}</div>', unsafe_allow_html=True)


def empty_state():
    st.markdown(
        '<div class="empty"><div class="big">🔍</div><h3>No categories match your filters</h3>'
        '<p>Loosen a filter or press <b>Reset filters</b> in the sidebar.</p></div>',
        unsafe_allow_html=True)


# ---------------------------------------------------------------- charts
def style_fig(fig, height=430, unified=False, legend=True):
    fig.update_layout(
        height=height,
        template="plotly_white",
        font=dict(family="Inter, sans-serif", size=13, color=TEXT),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=6, r=6, t=46 if legend else 18, b=6),
        hoverlabel=dict(bgcolor="white", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans-serif", size=13, color=TEXT)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title_text="",
                    bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        showlegend=legend,
        hovermode="x unified" if unified else "closest",
        barcornerradius=7,
        bargap=0.28,
    )
    fig.update_xaxes(showgrid=False, linecolor="#e2e8f0", zeroline=False, ticks="",
                     title_font=dict(size=12, color=MUTED))
    fig.update_yaxes(gridcolor="#eef1f6", zeroline=False, linecolor="rgba(0,0,0,0)",
                     title_font=dict(size=12, color=MUTED))
    return fig


def style_lines(fig):
    fig.update_traces(line=dict(width=3, shape="spline", smoothing=0.7),
                      marker=dict(size=8, line=dict(width=2, color="white")))
    return fig


def chart_card(fig, kind, key, title="", caption=""):
    """Plotly chart inside an animated white card. kind: line | bar | hbar | scatter."""
    with st.container(key=f"card_{kind}_{key}"):
        if title:
            section(title, caption)
        st.plotly_chart(fig, width="stretch", theme=None,
                        config={"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]})



# ---------------------------------------------------------------- sidebar filters
def _filter_defaults(kpis):
    lo = int(kpis["avg_monthly_clicks"].min())
    hi = int(kpis["avg_monthly_clicks"].max()) + 1
    return {"f_search": "", "f_season": [], "f_strength": [], "f_priority": [],
            "f_months": ("Jan", "Dec"), "f_clicks": (lo, hi)}


def _reset_filters(defaults):
    for k, v in defaults.items():
        st.session_state[k] = v


def init_filter_state(kpis):
    # re-assigning keeps the values alive on pages that don't show the filter widgets
    for k, v in _filter_defaults(kpis).items():
        st.session_state[k] = st.session_state.get(k, v)


def apply_filters(kpis):
    """Returns the KPI table filtered by the current sidebar selection."""
    # read only: the widgets own these keys, so they must not be written here
    s = {k: st.session_state.get(k, v) for k, v in _filter_defaults(kpis).items()}
    f = kpis
    if s["f_search"].strip():
        f = f[f.index.str.contains(s["f_search"].strip(), case=False, regex=False)]
    if s["f_season"]:
        f = f[f["peak_season"].isin(s["f_season"])]
    if s["f_strength"]:
        f = f[f["strength"].isin(s["f_strength"])]
    if s["f_priority"]:
        f = f[f["priority"].isin(s["f_priority"])]
    m_lo, m_hi = MONTH_NUM[s["f_months"][0]], MONTH_NUM[s["f_months"][1]]
    f = f[f["peak_month"].between(m_lo, m_hi)]
    return f[f["avg_monthly_clicks"].between(*s["f_clicks"])]


def render_sidebar(kpis, show_filters=True):
    """Brand block plus the shared filter widgets (filters apply to every data page)."""
    init_filter_state(kpis)
    sb = st.sidebar
    sb.markdown(
        '<div class="sb-brand"><div class="sb-logo">📅</div><div><div class="sb-name">smartbuy</div>'
        '<div class="sb-tag">Seasonality Explorer · 2021</div></div></div>', unsafe_allow_html=True)
    if not show_filters:
        sb.caption("Filters appear on the data pages (KPIs, Top clicks, Seasonality).")
        return

    defaults = _filter_defaults(kpis)
    sb.markdown('<div class="sb-title">Filters</div>', unsafe_allow_html=True)
    sb.text_input("🔎 Search category", key="f_search", placeholder="e.g. shoes, garden, toys …")
    sb.pills("Peak season", SEASON_ORDER, selection_mode="multi", key="f_season",
             format_func=lambda s: f"{SEASON_ICONS[s]} {s.capitalize()}")
    sb.pills("Seasonality strength", ["strong", "moderate", "flat"], selection_mode="multi",
             key="f_strength", format_func=str.capitalize)
    sb.multiselect("Priority group", list(PRIORITY_COLORS), key="f_priority", placeholder="All groups")
    # value= tells Streamlit this is a range slider (the session state value wins anyway)
    sb.select_slider("Peak month", options=MONTH_LIST, value=("Jan", "Dec"), key="f_months")
    lo, hi = defaults["f_clicks"]
    sb.slider("Avg. monthly clicks", lo, hi, key="f_clicks", step=max(1, (hi - lo) // 200))

    n = len(apply_filters(kpis))
    sb.markdown(
        f'<div class="sb-count"><b>{n}</b> of {len(kpis)} categories shown'
        f'<div class="sb-bar"><div style="width:{n / len(kpis) * 100:.1f}%"></div></div></div>',
        unsafe_allow_html=True)
    sb.button("↺  Reset filters", on_click=_reset_filters, args=(defaults,), width="stretch",
              disabled=n == len(kpis))
    sb.caption("Empty filter = everything selected. Filters apply to all pages.")
