# Contains all display related utils
from IPython.display import display, HTML

def hc(title: str, keywords: list[str]=[]):
    """
    Display header with calendar on the left side and vertically centered text.

    Parameters
    ----------
    title: str
        Title of the topic.
    keywords: list[str]
        Keywords related to the topic.

    Returns
    -------
    None
    """
    from datetime import datetime
    from IPython.display import display, HTML

    # Get current date and time
    now = datetime.now()
    day = now.strftime("%d")
    month = now.strftime("%b")
    year = now.strftime("%Y")
    time = now.strftime("%I:%M:%S %p")

    if len(keywords) == 0:
        keywords_str = ""
    else:
        keywords_str = "; ".join(keywords) + ";"

    html_code = f"""
    <div style="
        display: flex;
        align-items: center;
        font-family: 'Georgia', serif;
        border-left: 3px solid #ccc;
        padding-left: 12px;
        margin-bottom: 1em;
        gap: 20px;
    ">
        <!-- Calendar on the left -->
        <div style="
            display: inline-block;
            font-family: 'Arial', sans-serif;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 1px 1px 6px rgba(0,0,0,0.1);
            width: 120px;
            font-size: 12px;
            text-align: center;
            flex-shrink: 0;
        ">
            <!-- Last modified label -->
            <div style="
                background: #f4f4f4;
                color: #555;
                padding: 4px 0;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            ">
                Last modified
            </div>
            
            <!-- Main calendar -->
            <div>
                <div style="
                    background: #66a6ff;
                    color: white;
                    padding: 5px 0;
                    font-weight: bold;
                ">
                    {month}, {year}
                </div>
                <div style="
                    background: #fff;
                    color: #333;
                    padding: 8px 0;
                    font-size: 20px;
                    font-weight: bold;
                ">
                    {day}
                </div>
                <div style="
                    background: #f4f4f4;
                    color: #333;
                    padding: 4px 0;
                    font-size: 12px;
                ">
                    {time}
                </div>
            </div>
        </div>
        
        <!-- Header content on the right -->
        <div style="flex: 1;">
            <h2 style="
                margin: 0;
                color: #EF8C00;
                font-size: 2.4em;
                padding-left: 0;
                text-indent: 0;
            ">
                {title}
            </h2>
            <p style="margin: 0.5em 0 0 0;">
                {keywords_str}
            </p>
        </div>
    </div>
    """
    display(HTML(html_code))

def toc(tasks, done=0, title="Table of Contents"):
    """
    Floating, collapsible Table of Contents with hyperlinks and circular progress.
    Dark theme version: stays fixed at top-right, collapses into a progress circle.
    """
    def header_id(text: str) -> str:
        return text.replace(" ", "-")
    
    total = len(tasks)
    done = min(done, total)
    percent = int(done / total * 100)
    container_id = "toc-box"
    
    html_parts = []
    
    # Floating container box (dark theme, collapsed width first)
    html_parts.append(f"""
    <div id="{container_id}" style="
        position:fixed; 
        top:40px; right:10px; 
        background:#1e1e1e; 
        border-left:4px solid #4caf50; 
        border-radius:8px; 
        box-shadow:0 2px 8px rgba(0,0,0,0.35); 
        font-family:'Fira Code', Consolas, monospace;
        z-index:9999;
        width:50px; /* collapsed width */
        transition: width 0.3s ease;
        overflow:hidden;
        color:#d4d4d4;
    ">
    """)
    
    # Progress circle toggle
    html_parts.append(f"""
    <div onclick="
        var box=document.getElementById('{container_id}');
        var content=document.getElementById('{container_id}-content');
        if(content.style.display=='none'){{
            content.style.display='block';
            box.style.width='260px';
        }} else {{
            content.style.display='none';
            box.style.width='50px';
        }}
    " style="display:flex; align-items:center; justify-content:center; 
             padding:8px; cursor:pointer; user-select:none;">
        <svg width="32" height="32" viewBox="0 0 36 36" style="transform: rotate(-90deg);">
            <circle cx="18" cy="18" r="15.9155" fill="none" stroke="#333" stroke-width="3"/>
            <circle cx="18" cy="18" r="15.9155" fill="none" 
                    stroke="#4caf50" stroke-width="3"
                    stroke-dasharray="{percent}, 100"/>
            <text x="18" y="21" text-anchor="middle" fill="#d4d4d4"
                  font-size="9" font-family="Arial" transform="rotate(90,18,18)">{done}/{total}</text>
        </svg>
    </div>
    """)
    
    # Collapsible content container (hidden by default)
    html_parts.append(f"""
    <div id="{container_id}-content" style="display:none; padding:0 15px 12px 15px; 
                max-height:60vh; overflow-y:auto;">
        <div style="font-weight:bold; font-size:14px; margin-bottom:10px; color:#ffffff;">
            {title}
        </div>
    """)
    
    # Task list
    for i, task in enumerate(tasks):
        if i < done:
            dot_color, text_color, icon = "#4caf50", "#4caf50", "✓"
        else:
            dot_color, text_color, icon = "#2d2d2d", "#999", "○"
            
        connector = ""
        if i < len(tasks) - 1:
            line_color = "#4caf50" if i < done else "#444"
            connector = f'<div style="width:2px; height:20px; background:{line_color}; margin-left:9px; margin-top:-4px;"></div>'
            
        task_link = f'<a href="#{header_id(task)}" style="color:{text_color}; text-decoration:none;">{task}</a>'
        
        html_parts.append(f"""
        <div>
            <div style="display:flex; align-items:center; margin-bottom:0;">
                <div style="
                    width:20px; height:20px; border-radius:50%; 
                    background:{dot_color}; color:white; 
                    display:flex; align-items:center; justify-content:center;
                    font-size:10px; font-weight:bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.35);
                ">{icon}</div>
                <div style="margin-left:10px; font:12px 'Fira Code', monospace; font-weight:500;">
                    {task_link}
                </div>
            </div>
            {connector}
        </div>
        """)
        
    html_parts.append("</div></div>")
    display(HTML("".join(html_parts)))