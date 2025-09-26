from IPython.display import display, HTML
from datetime import datetime

def hc(title: str, keywords: list[str] = [""], link: str | None = None):
    """
    Display header with a dim calendar card (fits both dark & light modes).
    Optionally adds a link next to the title.
    """
    now = datetime.now()
    day = now.strftime("%d")
    month = now.strftime("%b")
    year = now.strftime("%Y")
    time = now.strftime("%I:%M:%S %p")

    keywords_str = "; ".join(keywords) + ";" if keywords else ""

    link_html = f"""<a href="{link}" target="_blank" class="hc-link">🔗</a>""" if link else ""

    html_code = f"""
    <style>
    .hc-wrapper {{
        display: flex;
        align-items: center;
        font-family: 'Georgia', serif;
        border-left: 3px solid #666;
        padding-left: 12px;
        margin-top: 1em;
        margin-bottom: 1em;
        gap: 20px;
    }}
    .hc-calendar {{
        display: inline-block;
        font-family: 'Arial', sans-serif;
        border-radius: 8px;
        overflow: hidden;
        background: #2d2d2d;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        width: 120px;
        font-size: 12px;
        text-align: center;
        flex-shrink: 0;
        border: 1px solid #444;
    }}
    .hc-header {{
        background: #333;
        color: #ddd;
        padding: 4px 0;
        font-weight: bold;
        font-size: 11px;
    }}
    .hc-month {{
        background: #EF8C00;
        color: #fff;
        padding: 5px 0;
        font-weight: bold;
    }}
    .hc-day {{
        background: #3a3a3a;
        color: #eee;
        padding: 8px 0;
        font-size: 20px;
        font-weight: bold;
    }}
    .hc-time {{
        background: #333;
        color: #bbb;
        padding: 4px 0;
        font-size: 12px;
    }}
    .hc-title {{
        margin: 0;
        color: #EF8C00;
        font-size: 1.8em;
        font-weight: 500;
        line-height: 1.2em;
        word-break: break-word;
    }}
    .hc-keywords {{
        margin: 0.5em 0 0 0;
        font-size: 0.9em;
        opacity: 0.8;
    }}
    .hc-link {{
        margin-left: 8px;
        font-size: 0.8em;
        color: #EF8C00 !important;
        text-decoration: none !important;
    }}
    .hc-link:hover {{
        color: #EF8C00 !important;
        text-decoration: none !important;
    }}
    </style>

    <div class="hc-wrapper">
        <!-- Calendar -->
        <div class="hc-calendar">
            <div class="hc-header">Last modified</div>
            <div class="hc-month">{month}, {year}</div>
            <div class="hc-day">{day}</div>
            <div class="hc-time">{time}</div>
        </div>
        
        <!-- Header text -->
        <div style="flex: 1;">
            <div class="hc-title">{title} {link_html}</div>
            <p class="hc-keywords">{keywords_str}</p>
        </div>
    </div>
    """
    display(HTML(html_code))
