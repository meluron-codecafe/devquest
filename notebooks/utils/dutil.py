# Contains all display related utils
from IPython.display import display, HTML

def hc(title: str, keywords: list[str] = [""]):
    """
    Display header with a dim calendar card (fits both dark & light modes).
    """
    from datetime import datetime
    from IPython.display import display, HTML

    now = datetime.now()
    day = now.strftime("%d")
    month = now.strftime("%b")
    year = now.strftime("%Y")
    time = now.strftime("%I:%M:%S %p")

    keywords_str = "; ".join(keywords) + ";" if keywords else ""

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
            <div class="hc-title">{title}</div>
            <p class="hc-keywords">{keywords_str}</p>
        </div>
    </div>
    """
    display(HTML(html_code))




def toc(tasks, title="Quick Navigation"):
    """
    TOC button styled exactly like the theme toggle button.
    Appears to the left of the theme toggle.
    Works in both light and dark mode.
    """
    from IPython.display import HTML, display

    def header_id(text: str) -> str:
        return text.replace(" ", "-").replace(".", "")

    total = len(tasks)

    html = f"""
    <!-- TOC Trigger -->
    <button id="toc-trigger" class="toc-toggle" onclick="toggleCommandPalette()" title="Open TOC">
      ☰
    </button>

    <!-- Command Palette -->
    <div id="cmd-palette" style="
	    position: fixed;
	    top: 50%;
	    left: 50%;
	    transform: translate(-50%, -50%) scale(0.9);
	    width: 90%;
	    max-width: 450px;
	    min-width: 280px;
	    background: rgba(20, 20, 20, 0.98);
	    border: 1px solid rgba(255,255,255,0.1);
	    border-radius: 8px;
	    backdrop-filter: blur(20px);
	    z-index: 1001;
	    opacity: 0;
	    visibility: hidden;
	    transition: all 0.2s ease;
	    font-family: 'Monaco', 'Menlo', monospace;
	    font-size: 13px;
	">
        <!-- Header -->
        <div style="
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.7);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span>{title}</span>
            <span>{total} sections</span>
        </div>

        <!-- Navigation Items -->
        <div style="max-height: 300px; overflow-y: auto;" id="nav-items">
    """

    for i, task in enumerate(tasks):
        html += f"""
        <a href="#{header_id(task)}" onclick="closeCommandPalette()" 
           class="nav-item" style="
            display: flex;
            align-items: center;
            padding: 10px 16px;
            text-decoration: none;
            color: rgba(255,255,255,0.85);
            transition: all 0.2s ease;
            border-left: 2px solid transparent;
        " onmouseover="
            this.style.background = 'rgba(255,255,255,0.05)';
            this.style.borderLeftColor = '#4aa3ff';
        " onmouseout="
            this.style.background = 'transparent';
            this.style.borderLeftColor = 'transparent';
        ">
            <span style="
                color: rgba(255,255,255,0.6);
                margin-right: 12px;
                width: 20px;
                text-align: center;
                font-size: 12px;
            ">{i + 1:02d}</span>
            <span style="flex: 1;">{task}</span>
        </a>
        """

    html += """
        </div>
    </div>

    <!-- Overlay -->
    <div id="cmd-overlay" onclick="closeCommandPalette()" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
        opacity: 0;
        visibility: hidden;
        transition: all 0.2s ease;
    "></div>

    <script>
    function toggleCommandPalette() {
        const palette = document.getElementById('cmd-palette');
        const overlay = document.getElementById('cmd-overlay');

        if (palette.style.visibility === 'visible') {
            closeCommandPalette();
        } else {
            overlay.style.opacity = '1';
            overlay.style.visibility = 'visible';
            palette.style.opacity = '1';
            palette.style.visibility = 'visible';
            palette.style.transform = 'translate(-50%, -50%) scale(1)';
        }
    }

    function closeCommandPalette() {
        const palette = document.getElementById('cmd-palette');
        const overlay = document.getElementById('cmd-overlay');

        palette.style.opacity = '0';
        palette.style.transform = 'translate(-50%, -50%) scale(0.9)';
        overlay.style.opacity = '0';

        setTimeout(() => {
            palette.style.visibility = 'hidden';
            overlay.style.visibility = 'hidden';
        }, 200);
    }

    // Keyboard shortcut (Cmd/Ctrl + K)
    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            toggleCommandPalette();
        }
        if (e.key === 'Escape') {
            closeCommandPalette();
        }
    });
    </script>

    <style>
    /* TOC Trigger styled same as theme-toggle */
    .toc-toggle {
      position: fixed;
      top: 20px;
      right: 80px;  /* left of theme-toggle */
      background: #2d2d2d;
      color: #d4d4d4;
      border: 2px solid #444;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      cursor: pointer;
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      transition: all 0.3s ease;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .toc-toggle:hover {
      background: #3a3a3a;
      transform: scale(1.1);
    }

    /* Light mode styling for TOC trigger + palette */
    body.light-mode .toc-toggle {
      background: #f5f5f5;
      color: #333;
      border-color: #ddd;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    body.light-mode .toc-toggle:hover {
      background: #e0e0e0;
    }
    body.light-mode #cmd-palette {
      background: rgba(255, 255, 255, 0.98) !important;
      border-color: rgba(0,0,0,0.1) !important;
      color: #333 !important;
    }
    body.light-mode #cmd-palette .nav-item {
      color: rgba(0,0,0,0.85) !important;
    }
    body.light-mode #cmd-palette .nav-item span:first-child {
      color: rgba(0,0,0,0.5) !important;
    }
    body.light-mode #cmd-palette .nav-item:hover {
      background: rgba(0,0,0,0.05) !important;
    }
    body.light-mode #cmd-palette div[style*="border-bottom"] {
      border-bottom-color: rgba(0,0,0,0.1) !important;
      color: rgba(0,0,0,0.7) !important;
    }
    </style>
    """

    display(HTML(html))
