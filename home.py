import pandas as pd
import streamlit as st
from Styles import get_custom_css, style_fig, donut_kpi
import plotly.express as px
import plotly.graph_objects as go
import json
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import sqlite3

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Bird Species Observation Dashboard",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Colors ----
PINK = "#f472b6"
BLUE = "#38bdf8"
PURPLE = "#a78bfa"
GREEN = "#6ee7b7"
YELLOW = "#FFFDD0"
WHITE = "#FAFAFA"
BLACK = "#000000"
BG = "#0d0d26"
CARD_BG = "#181836"

PALETTE = [PINK, BLUE, PURPLE, GREEN, "#fbbf24", "#fb7185"]

st.markdown(get_custom_css(BG, CARD_BG, PINK, BLUE, PURPLE, GREEN, YELLOW, WHITE, BLACK), unsafe_allow_html=True)

# =========================================================
# Load -Data from SQLite database
# =========================================================
@st.cache_data
def load_data():
    conn = sqlite3.connect("bird_data.db")
    df = pd.read_sql_query("SELECT * FROM observations", conn)
    conn.close()
    df["Date"] = pd.to_datetime(df["Date"])
    return df

bird_df = load_data()

# ---- Default page = Home ----
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("🧭 Navigation")
k1, k2, k3 = st.sidebar.columns(3)
with k1:
    if st.button("🏠", help="Home",use_container_width=True):
        st.session_state.page = "Home"
with k2:
    if st.button("📊", help="Analysis", use_container_width=True):
        st.session_state.page = "Analysis"
with k3:
    if st.button("💡", help="Insights", use_container_width=True):
        st.session_state.page = "Insights"
st.sidebar.divider()
st.sidebar.title("🔍 Filters")
habitat_opt = st.sidebar.multiselect("Habitat", sorted(bird_df["Habitat"].dropna().unique()), default=[])
admin_opt = st.sidebar.multiselect("Admin Unit", sorted(bird_df["Admin_Unit"].dropna().unique()), default=[])
year_opt = st.sidebar.multiselect("Year", sorted(bird_df["Year"].dropna().unique()), default=[])
species_opt = st.sidebar.multiselect("Species (optional)", sorted(bird_df["Common_Name"].dropna().unique()))

df = bird_df.copy()
if habitat_opt:
    df = df[df["Habitat"].isin(habitat_opt)]
if admin_opt:
    df = df[df["Admin_Unit"].isin(admin_opt)]
if year_opt:
    df = df[df["Year"].isin(year_opt)]
if species_opt:
    df = df[df["Common_Name"].isin(species_opt)]
# =========================================================
# IF Home -> show landing page ONLY
# =========================================================
if st.session_state.page == "Home":
    
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
           return json.load(f)
    
    lottie_data = load_lottiefile("animation.json")
   # CSS for Lottie area
    lottie_html = f"""
    <div id="lottie-container" style="width:70px; height:70px; background:transparent; margin-top:-15px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
    <script>
    var animData = {json.dumps(lottie_data)};
    lottie.loadAnimation({{
        container: document.getElementById('lottie-container'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: animData
    }});
    </script>
    """
    col1, col2 = st.columns([0.8, 6], gap="small")
    with col1:
        components.html(lottie_html, height=80, width=80)

    with col2:
        st.title("Bird Species Data Analysis")
        st.caption("Forest & Grassland monitoring — Wildlife conservation, land management, eco-tourism, and policy insights")
            
    st.divider()  
    total_obs = len(df)
    unique_species = df["Common_Name"].nunique()
    unique_plots = df["Plot_Name"].nunique()
    watchlist_pct = round((df["PIF_Watchlist_Status"] == True).mean() * 100) if total_obs else 0
    flyover_pct = round((df["Flyover_Observed"] == True).mean() * 100) if total_obs else 0

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Total Observations", f"{total_obs:,}")
    with k2:
        st.metric("Unique Species", unique_species)
    with k3:
        st.metric("Plots Surveyed", unique_plots)
    k4,k5=st.columns(2)
    with k4:
        st.plotly_chart(donut_kpi("Watchlist %", "watchlist", watchlist_pct, PINK), use_container_width=False, config={"displayModeBar": False})
        st.caption("PIF Watchlist Species")
    with k5:
        st.plotly_chart(donut_kpi("Flyover %", "flyover", flyover_pct, BLUE), use_container_width=False, config={"displayModeBar": False})
        st.caption("Flyover Observations")
# =========================================================
# ELSE (Analysis) -> show dashboard ONLY after button click
# =========================================================
elif st.session_state.page == "Analysis":
    # ============================================
    # TABS FOR EACH ANALYSIS TYPE
    # ============================================
    st.title("🐦 Bird Species Observation Dashboard")
    st.divider()
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📅 Temporal","🌍 Spatial", "🐦 Species", "🌡️ Environmental",
        "📏 Distance & Behavior", "👤 Observer Trends", "🛡️ Conservation"
    ])
    
     # -------------------- TAB 1: TEMPORAL --------------------
    with tab1:
        st.subheader("Observation Frequency by Year, Month & Season")
        c1, c2 = st.columns(2)
        with c1:
            by_year = df.groupby("Year")["Common_Name"].count().reset_index()
            by_year.columns = ["Year", "Observations"]
            fig = px.line(by_year, x="Year", y="Observations", markers=True,
                          color_discrete_sequence=[PINK])
            st.plotly_chart(style_fig(fig, "Observations by Year"), use_container_width=True)
        with c2:
            by_season = df.groupby("Season")["Common_Name"].count().reindex(
                ["Winter", "Spring", "Summer", "Fall"]).reset_index()
            by_season.columns = ["Season", "Observations"]
            fig = px.bar(by_season, x="Season", y="Observations", color="Season",
                            color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Observations by Season"), use_container_width=True)
    
        by_month = df.groupby("Month_Name")["Common_Name"].count().reindex(
            ["January","February","March","April","May","June","July","August","September","October","November","December"]
        ).dropna().reset_index()
        by_month.columns = ["Month", "Observations"]
        fig = px.bar(by_month, x="Month", y="Observations", color_discrete_sequence=[PURPLE])
        st.plotly_chart(style_fig(fig, "Observations by Month"), use_container_width=True)
    
        st.subheader("Observation Time Windows")
        by_hour = df.groupby("Start_Hour")["Common_Name"].count().reset_index()
        by_hour.columns = ["Start_Hour", "Observations"]
        fig = px.area(by_hour, x="Start_Hour", y="Observations", color_discrete_sequence=[GREEN])
        st.plotly_chart(style_fig(fig, "Bird Activity by Start Hour"), use_container_width=True)
    
        st.subheader("Year × Month Heatmap")
        heat = df.dropna(subset=["Year", "Month"]).groupby(["Year", "Month"])["Common_Name"].count().reset_index()
        heat_pivot = heat.pivot(index="Year", columns="Month", values="Common_Name").fillna(0)
        fig = px.imshow(heat_pivot, color_continuous_scale="Magma", aspect="auto",
                            labels=dict(x="Month", y="Year", color="Observations"))
        st.plotly_chart(style_fig(fig, "Temporal Heatmap: Observations by Year & Month"), use_container_width=True)
    
    # -------------------- TAB 2: SPATIAL --------------------
    with tab2:
        st.subheader("Species Distribution Across Admin Units & Habitat Types")
        c1, c2 = st.columns(2)
        with c1:
            by_unit = df.groupby("Admin_Unit")["Common_Name"].nunique().sort_values(ascending=False).reset_index()
            by_unit.columns = ["Admin_Unit", "Unique_Species"]
            fig = px.bar(by_unit, x="Admin_Unit", y="Unique_Species", color="Admin_Unit",
                         color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Unique Species by Admin Unit"), use_container_width=True)
        with c2:
            by_habitat = df.groupby("Habitat")["Common_Name"].nunique().reset_index()
            by_habitat.columns = ["Habitat", "Unique_Species"]
            fig = px.pie(by_habitat, names="Habitat", values="Unique_Species", hole=0.55,
                         color_discrete_sequence=[GREEN, PURPLE])
            st.plotly_chart(style_fig(fig, "Species Diversity by Habitat"), use_container_width=True)
    
        st.subheader("Location & Plot-Level Insights")
        c3, c4 = st.columns(2)
        with c3:
            by_loc = df.groupby("Location_Type")["Common_Name"].nunique().sort_values(ascending=False).reset_index()
            by_loc.columns = ["Location_Type", "Unique_Species"]
            fig = px.bar(by_loc, x="Location_Type", y="Unique_Species", color="Location_Type",
                         color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Biodiversity Hotspots by Location Type"), use_container_width=True)
        with c4:
            top_plots = df.groupby("Plot_Name")["Common_Name"].nunique().sort_values(ascending=False).head(15).reset_index()
            top_plots.columns = ["Plot_Name", "Unique_Species"]
            fig = px.bar(top_plots, x="Unique_Species", y="Plot_Name", orientation="h",
                         color_discrete_sequence=[BLUE])
            fig.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(style_fig(fig, "Top 15 Plots by Species Diversity"), use_container_width=True)
    # -------------------- TAB 3: SPECIES --------------------
    with tab3:
        st.subheader("Diversity Metrics")
        c1, c2 = st.columns(2)
        with c1:
            top_species = df["Common_Name"].value_counts().head(15).reset_index()
            top_species.columns = ["Species", "Count"]
            fig = px.bar(top_species, x="Count", y="Species", orientation="h",
                         color_discrete_sequence=[PINK])
            fig.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(style_fig(fig, "Top 15 Most Observed Species"), use_container_width=True)
        with c2:
            species_by_loc = df.groupby("Location_Type")["Scientific_Name"].nunique().reset_index()
            species_by_loc.columns = ["Location_Type", "Unique_Species"]
            fig = px.pie(species_by_loc, names="Location_Type", values="Unique_Species", hole=0.55,
                         color_discrete_sequence=[GREEN, BLUE])
            st.plotly_chart(style_fig(fig, "Species Distribution by Location Type"), use_container_width=True)
    
        st.subheader("Activity Patterns & Gender Ratio")
        c3, c4 = st.columns(2)
        with c3:
            id_method = df["ID_Method"].value_counts().reset_index()
            id_method.columns = ["ID_Method", "Count"]
            fig = px.bar(id_method, x="ID_Method", y="Count", color="ID_Method",
                         color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Activity Type (ID Method) Frequency"), use_container_width=True)
        with c4:
            sex_ratio = df["Sex"].value_counts().reset_index()
            sex_ratio.columns = ["Sex", "Count"]
            fig = px.pie(sex_ratio, names="Sex", values="Count", hole=0.55,
                         color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Gender Ratio of Observations"), use_container_width=True)
    
    # -------------------- TAB 4: ENVIRONMENTAL --------------------
    with tab4:
        st.subheader("Weather Correlation with Observations")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x="Temperature", nbins=20, color_discrete_sequence=[PINK])
            st.plotly_chart(style_fig(fig, "Temperature Distribution"), use_container_width=True)
        with c2:
            fig = px.histogram(df, x="Humidity", nbins=20, color_discrete_sequence=[BLUE])
            st.plotly_chart(style_fig(fig, "Humidity Distribution"), use_container_width=True)
    
        c3, c4 = st.columns(2)
        with c3:
            sky = df["Sky"].value_counts().reset_index()
            sky.columns = ["Sky", "Count"]
            fig = px.bar(sky, x="Sky", y="Count", color="Sky", color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Observations by Sky Condition"), use_container_width=True)
        with c4:
            disturbance = df["Disturbance"].value_counts().reset_index()
            disturbance.columns = ["Disturbance", "Count"]
            fig = px.bar(disturbance, x="Disturbance", y="Count", color="Disturbance",
                         color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Disturbance Effect on Sightings"), use_container_width=True)
    
        st.subheader("Temperature vs Observation Count")
        temp_bins = pd.cut(df["Temperature"], bins=10)
        temp_activity = df.groupby(temp_bins.astype(str))["Common_Name"].count().reset_index()
        temp_activity.columns = ["Temperature_Range", "Observations"]
        fig = px.bar(temp_activity, x="Temperature_Range", y="Observations", color_discrete_sequence=[GREEN])
        st.plotly_chart(style_fig(fig, "Bird Activity Across Temperature Ranges"), use_container_width=True)
    
    # -------------------- TAB 5: DISTANCE & BEHAVIOR --------------------
    with tab5:
        st.subheader("Distance Analysis")
        c1, c2 = st.columns(2)
        with c1:
            dist_counts = df["Distance"].value_counts().reset_index()
            dist_counts.columns = ["Distance", "Count"]
            fig = px.bar(dist_counts, x="Distance", y="Count", color="Distance",
                         color_discrete_sequence=PALETTE)
            st.plotly_chart(style_fig(fig, "Observations by Distance Band"), use_container_width=True)
        with c2:
            flyover = df["Flyover_Observed"].value_counts().reset_index()
            flyover.columns = ["Flyover_Observed", "Count"]
            fig = px.pie(flyover, names="Flyover_Observed", values="Count", hole=0.55,
                         color_discrete_sequence=[BLUE, PURPLE])
            st.plotly_chart(style_fig(fig, "Flyover Frequency"), use_container_width=True)
    
        st.subheader("Species Typically Observed Closer vs Farther")
        top_n = df["Common_Name"].value_counts().head(10).index
        dist_species = df[df["Common_Name"].isin(top_n)]
        fig = px.histogram(dist_species, x="Common_Name", color="Distance", barmode="stack",
                            color_discrete_sequence=PALETTE)
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(style_fig(fig, "Distance Bands for Top 10 Species"), use_container_width=True)
        
    # -------------------- TAB 6: OBSERVER TRENDS --------------------
    with tab6:
        st.subheader("Observer Bias & Visit Patterns")
        c1, c2 = st.columns(2)
        with c1:
            obs_counts = df["Observer"].value_counts().head(15).reset_index()
            obs_counts.columns = ["Observer", "Observations"]
            fig = px.bar(obs_counts, x="Observations", y="Observer", orientation="h",
                         color_discrete_sequence=[PINK])
            fig.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(style_fig(fig, "Top 15 Observers by Observation Count"), use_container_width=True)
        with c2:
            visit_species = df.groupby("Visit")["Common_Name"].nunique().reset_index()
            visit_species.columns = ["Visit", "Unique_Species"]
            fig = px.bar(visit_species, x="Visit", y="Unique_Species", color_discrete_sequence=[GREEN])
            st.plotly_chart(style_fig(fig, "Species Diversity by Visit Number"), use_container_width=True)
    
    # -------------------- TAB 7: CONSERVATION --------------------
    with tab7:
        st.subheader("Watchlist & Stewardship Trends")
        c1, c2 = st.columns(2)
        with c1:
            watchlist_species = df[df["PIF_Watchlist_Status"] == True]["Common_Name"].value_counts().head(15).reset_index()
            watchlist_species.columns = ["Species", "Count"]
            fig = px.bar(watchlist_species, x="Count", y="Species", orientation="h",
                         color_discrete_sequence=[PINK])
            fig.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(style_fig(fig, "Top Watchlist Species by Sightings"), use_container_width=True)
        with c2:
            watchlist_trend = df[df["PIF_Watchlist_Status"] == True].groupby("Year")["Common_Name"].count().reset_index()
            watchlist_trend.columns = ["Year", "Watchlist_Sightings"]
            fig = px.line(watchlist_trend, x="Year", y="Watchlist_Sightings", markers=True,
                          color_discrete_sequence=[PURPLE])
            st.plotly_chart(style_fig(fig, "Watchlist Species Sightings Over Time"), use_container_width=True)
    
        st.subheader("AOU Code Distribution (Top 20)")
        aou = df["AOU_Code"].value_counts().head(20).reset_index()
        aou.columns = ["AOU_Code", "Count"]
        fig = px.bar(aou, x="AOU_Code", y="Count", color_discrete_sequence=[BLUE])
        st.plotly_chart(style_fig(fig, "Most Frequent AOU Codes"), use_container_width=True)
    
    st.divider()
    st.caption("Bird Species Observation Dashboard — Forest & Grassland Monitoring Data")
# =========================================================
# ELSE (Insight) 
# =========================================================
elif st.session_state.page == "Insights":
    st.title("💡 Insights & Recommendations")
    st.caption("Key findings automatically generated from the monitoring data")

    # ---- Compute dynamic insights from the FULL dataset ----
    top_habitat = bird_df.groupby("Habitat")["Common_Name"].nunique().idxmax()
    top_season = bird_df["Season"].value_counts().idxmax()
    top_admin_unit = bird_df.groupby("Admin_Unit")["Common_Name"].nunique().idxmax()
    watchlist_species = bird_df[bird_df["PIF_Watchlist_Status"] == True]["Common_Name"].value_counts()
    top_watchlist_species = watchlist_species.idxmax() if not watchlist_species.empty else "N/A"
    flyover_rate = round((bird_df["Flyover_Observed"] == True).mean() * 100, 1)

    st.markdown(f"""
    - 🌳 **{top_habitat}** habitat shows the highest species diversity — prioritize this habitat type for conservation and land management efforts.
    - 📅 **{top_season}** has the highest observation frequency — a strong season for eco-tourism and bird-watching promotion.
    - 📍 **{top_admin_unit}** has the greatest species diversity among all admin units — a strong candidate for a biodiversity hotspot designation.
    - 🛡️ **{top_watchlist_species}** is the most frequently observed species on the PIF Watchlist — recommend targeted monitoring and habitat protection.
    - ✈️ **{flyover_rate}%** of all observations were flyovers (birds passing through, not using the habitat) — the remaining {100 - flyover_rate:.1f}% represent confirmed habitat use, a more reliable indicator for land management decisions.
    """)

    st.divider()
    st.subheader("Recommendations")
    st.markdown(f"""
    1. Focus conservation funding on **{top_habitat}** habitat and **{top_admin_unit}**, given their high species diversity.
    2. Schedule eco-tourism bird-watching campaigns around **{top_season}**, when activity peaks.
    3. Prioritize protective measures for **{top_watchlist_species}** and other PIF Watchlist species detected in the data.
    4. Use non-flyover observations as the primary signal for habitat quality assessments, since flyovers don't confirm actual habitat use.
    """)
