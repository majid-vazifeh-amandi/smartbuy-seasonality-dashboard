# Entry point of the smartbuy seasonality app:  streamlit run app.py
# Sets up the theme, the page navigation and the shared sidebar filters.
import streamlit as st

from ui import render_sidebar, setup_page
from utils import load_data

setup_page("smartbuy Seasonality", "📅")

monthly, seasonal, kpis, monthly_long = load_data()

home = st.Page("views/home.py", title="Project summary", icon="🏠", default=True)
pages = [
    home,
    st.Page("views/kpis.py", title="KPIs", icon="📊"),
    st.Page("views/top_clicks.py", title="Top clicks", icon="🏆"),
    st.Page("views/seasonality.py", title="It's all about seasonality", icon="🌦️"),
]
page = st.navigation(pages)

render_sidebar(kpis, show_filters=page is not home)
page.run()
