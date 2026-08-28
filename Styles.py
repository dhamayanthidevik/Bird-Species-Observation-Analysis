from tkinter import font


def get_custom_css(BG, CARD_BG, PINK, BLUE, PURPLE, GREEN,YELLOW, WHITE, BLACK):
 return f"""
<style>
    .stApp {{
        background-color: {BG};
        color: #ffffff;
    }}
    header[data-testid="stHeader"]{{
    background-color: {BG};
    }}
    section[data-testid="stSidebar"] {{  /*OUTER*/
        background-color: {PINK};
        border-right: 3px solid {PINK};
    }}
    section[data-testid="stSidebar"] > div {{/*inner Filter*/
        background-color: {BG};
        label {{
            color: #e5e7eb;
        }}
    }}
    div[data-testid="stToolbar"] {{
        background-color: {BG};
    }}
    div[data-baseweb="select"] > div {{
    background-color: {BG} !important;
    border-color: {PINK} !important;
    }}
    hr {{  /* horizontal rule */
    border: none !important;
    border-top: 3px solid {PINK} !important;
    width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    }}
    hr {{
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
    }}
    section[data-testid="stSidebar"] hr {{
    margin-top: 10px !important;
    margin-bottom: 20px !important;
    }}
    .stTabs {{
    margin-top: -1rem !important;
    }}
    /*----------------- Tabs Styling------------------------- */
    .stTabs [data-baseweb="tab-list"]{{
    gap: 12px !important;
    background-color: {YELLOW} !important;
    color:{GREEN} !important;
    padding: 5px 10px 5px 10px !important;
    border-radius: 12px 12px 0 0 !important;
    border-bottom: 3px solid {WHITE} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
    background-color: {CARD_BG} !important;
    border-radius: 20px !important;
    padding: 5px 5px !important;
    border: 1px solid {BLUE} !important;
    white-space: nowrap;
    min-height: unset !important;
    height: auto !important;
    }}
    .stTabs [data-baseweb="tab"] p {{
    color: {WHITE} !important;
    font-weight: 500 !important;
    }}
    .stTabs [aria-selected="true"] {{
    background-color: {BLUE} !important;
    border: 1px solid {BLUE} !important;
    border-radius: 0 0 20px 20px !important;
    padding: 10px 20px !important;
    min-height: unset !important;
    height: auto !important;
    }}
    .stTabs [aria-selected="true"] p {{
    color: {BLACK} !important;
    font-weight: 700 !important;
    margin: 0 !important;
    line-height: 1 !important;
    }}
    .stTabs [data-testid="stMarkdownContainer"] {{
    padding: 0 !important;
    margin: 0 !important;
    color: {WHITE} !important;
    }}
    /*----------------- Remove Selection Indicator from Tabs------------------------- */
    [data-testid="stTab"] .react-aria-SelectionIndicator {{
      display: none !important;
    }}
    /*----------------- Metric Styling------------------------- */
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG} !important;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #2e2e55;
    }}
    div[data-testid="stMetric"] label {{
        color: {WHITE} !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {WHITE} !important;
    }}
    div[data-testid="stMetricDelta"] {{
        color: {GREEN} !important;
    }}
    /*-----------------To change the Navigation, Filters, and Plot Container heading color------*/
    /*----------------- Navigation Heading Styling------------------------- */
    div[data-testid="stElementContainer"]:has(
    [data-testid="stHeading"] h1
    ) {{
    background-color: #0d0d26 !important;
    border-radius: 8px !important;
    padding: 8px !important;
    color: {WHITE} !important;
    }}
    /*----------------- Font in slidebar Styling------------------------- */
    /* Placeholder text ("Choose options") + typed input text */
    div[data-baseweb="select"] input {{
        font-family: 'Georgia', serif !important;
        font-size: 15px !important;
        color: #ffffff !important;
    }}

    /* Placeholder specifically (before anything is typed/selected) */
    div[data-baseweb="select"] div[class*="placeholder"] {{
        font-family: 'Georgia', serif !important;
        font-size: 15px !important;
        color: #ffffff !important;
    }}
    /* Outer chip background (the actual colored pill) */
    span[data-baseweb="tag"] {{
        background-color: {BG} !important;
        border: 1px solid {WHITE} !important;
        
    }}
    /* Inner text inside the chip */
    /* Selected tag chips (e.g. "Forest", "2018") */
    span[data-baseweb="tag"] span {{
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        background-color: {BG} !important;
        color: {WHITE} !important;
    }}

    /* Options shown when dropdown is opened */
    div[data-baseweb="popover"] li {{
        font-family: 'Georgia', serif !important;
        font-size: 15px !important;
        background-color: {BG} !important;
        color: {WHITE} !important;
    }}
    /* Placeholder text ("Choose options") */
    div[data-baseweb="select"] div[class*="placeholder"] {{
        color: #ffffff !important;
    }}

    /* The dropdown arrow icon next to it */
    div[data-baseweb="select"] svg {{
        fill: #ffffff !important;
        color: #ffffff !important;
    }}
    /*----------------- Plotly Chart Styling------------------------- */
    div[data-testid="stPlotlyChart"] {{
        border: 1px solid {GREEN} !important;
        border-radius: 12px !important;
        padding: 10px !important;
        overflow: visible !important;
        color: {WHITE} !important;
    }}
    div[data-testid="stCustomComponentV1"] {{
        background-color: {BLUE} !important;
        mix-blend-mode: multiply;
        border-radius: 8px;
        color: {WHITE} !important;
    }}
    /*----------------- Sidebar Button Styling------------------------- */
    section[data-testid="stSidebar"] button {{
        font-size: 28px !important;
        padding: 16px !important;
        height: 30px !important;
        width: 30% !important;
        background-color: {BG} !important;
        color: {WHITE} !important;
    }}
section[data-testid="stSidebar"] button p {{
    font-size: 28px !important;
    color: {WHITE} !important;
}} 
/* Move Lottie animation upward */
div[data-testid="stElementContainer"]:has(
    [data-testid="stLottieAnimation"]
) {{
    margin-top: -150px !important;
}}
/*-----------------title move to upper------------------------- */
div[data-testid="stHeading"] h1 {{
    margin-top: -50px !important;
}}

</style>
"""
from django.contrib.admin import display
import plotly.graph_objects as go
def donut_kpi(label, value, pct, color):
    fig = go.Figure(go.Pie(
        values=[pct, 100 - pct],
        hole=0.75,
        marker_colors=[color, "#ECECE6"],
        showlegend=False,
        textinfo="none",
    ))
    fig.update_layout(
        annotations=[dict(text=f"{pct}%", x=0.5, y=0.5, font_size=22, font_color="white", showarrow=False)],
        margin=dict(l=0, r=0, t=0, b=0),
        height=150,
        width=1000,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
def style_fig(fig, title=None):
    # fig.update_layout(
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     paper_bgcolor="rgba(0,0,0,0)",
    #     font_color="#e5e7eb",
    #     title=title,
    #     margin=dict(l=10, r=10, t=40, b=10),
    fig.update_layout(
        
        title=dict(
            font=dict(
                color="#E8F4F5",
                size=16
            )
        ),

        font=dict(
            family="Source Sans",
            color="#E8F4F5",
            size=12
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        # paper_bgcolor="#031B2E",
        # plot_bgcolor="#031B2E",

        xaxis=dict(
            title_font=dict(
                color="#8FA6B2",
                size=14
            ),
            tickfont=dict(
                color="#8FA6B2",
                size=12
            ),
            gridcolor="#29404D",
            zerolinecolor="#29404D"
        ),

        yaxis=dict(
            title_font=dict(
                color="#8FA6B2",
                size=14
            ),
            tickfont=dict(
                color="#8FA6B2",
                size=12
            ),
            gridcolor="#29404D",
            zerolinecolor="#29404D"
        ),

        legend=dict(
            font=dict(
                color="#E8F4F5",
                size=12
            ),
            title_font=dict(
                color="#E8F4F5",
                size=12
            )
        )
    )
    
    return fig

