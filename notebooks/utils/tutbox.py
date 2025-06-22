from IPython.display import HTML

def tutbox(content, box_type="note", title=None):
    """
    Generate a tutorial information box for Jupyter notebooks.
    """
    box_configs = {
        'note': ('📝', '#0d47a1', '#e3f2fd', '#2196f3', 'Note'),
        'tip': ('💡', '#1b5e20', '#e8f5e8', '#4caf50', 'Tip'),
        'question': ('❓', '#6a1b9a', '#f3e5f5', '#9c27b0', 'Question'),
        'warning': ('⚠️', '#e65100', '#fff3e0', '#ff9800', 'Warning'),
        'danger': ('🚨', '#b71c1c', '#ffebee', '#f44336', 'Danger'),
        'important': ('⭐', '#4a148c', '#f3e5f5', '#9c27b0', 'Important'),
        'example': ('📋', '#004d40', '#e0f2f1', '#009688', 'Example'),
        'exercise': ('🏋️', '#1a237e', '#e8eaf6', '#3f51b5', 'Exercise'),
        'success': ('✅', '#33691e', '#f1f8e9', '#8bc34a', 'Success'),
        'info': ('ℹ️', '#006064', '#e0f7fa', '#00bcd4', 'Info'),
        'code': ('💻', '#263238', '#f5f5f5', '#607d8b', 'Code'),
        'upcoming': ('🔜', '#1565c0', '#e3f2fd', '#42a5f5', 'Coming Up Next')
    }

    if box_type not in box_configs:
        available = ', '.join(box_configs.keys())
        raise ValueError(f"Invalid box_type '{box_type}'. Available types: {available}")
    
    icon, text_color, bg_color, border_color, default_title = box_configs[box_type]
    display_title = title if title is not None else default_title

    html = f"""
    <div style="
        margin: 15px 0; 
        padding: 16px 20px; 
        border-radius: 8px; 
        border-left: 4px solid {border_color}; 
        display: flex; 
        align-items: flex-start; 
        gap: 12px; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); 
        background-color: {bg_color}; 
        color: {text_color};
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
        <div style="
            font-size: 20px; 
            margin-top: 2px; 
            flex-shrink: 0;
        ">{icon}</div>
        <div style="flex: 1;">
            <div style="
                font-weight: bold; 
                margin-bottom: 6px; 
                font-size: 14px; 
                text-transform: uppercase; 
                letter-spacing: 0.5px;
            ">{display_title}</div>
            <div style="
                margin: 0; 
                font-size: 14px; 
                line-height: 1.5;
            ">{content}</div>
        </div>
    </div>
    """
    return HTML(html)

# Convenience wrappers
def note(content, title=None): return tutbox(content, "note", title)
def warning(content, title=None): return tutbox(content, "warning", title)
def exercise(content, title=None): return tutbox(content, "exercise", title)
def question(content, title=None): return tutbox(content, "question", title)
def upcoming(content, title=None): return tutbox(content, "upcoming", title)

def nav(prev_link=None, next_link=None, prev_content="Previous Section", next_content="Next Section", title="Navigation"):
    """
    Generate a navigation box with previous and next links.
    """
    prev_html = (
        f'<a href="{prev_link}" style="color: #5d4037; text-decoration: none; padding: 8px 12px; border-radius: 4px; background-color: #efebe9; border: 1px solid #8d6e63; display: inline-block; font-weight: 500;">⬅️ {prev_content}</a>'
        if prev_link else
        f'<span style="color: #999; padding: 8px 12px;">⬅️ {prev_content}</span>'
    )

    next_html = (
        f'<a href="{next_link}" style="color: #2e7d32; text-decoration: none; padding: 8px 12px; border-radius: 4px; background-color: #e8f5e8; border: 1px solid #66bb6a; display: inline-block; font-weight: 500;">{next_content} ➡️</a>'
        if next_link else
        f'<span style="color: #999; padding: 8px 12px;">{next_content} ➡️</span>'
    )

    html = f"""
    <div style="
        margin: 15px 0; 
        padding: 16px 20px; 
        border-radius: 8px; 
        border-left: 4px solid #607d8b; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); 
        background-color: #f8f9fa; 
        color: #37474f;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
        <div style="
            font-weight: bold; 
            margin-bottom: 12px; 
            font-size: 14px; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="font-size: 18px;">🧭</span>
            {title}
        </div>
        <div style="
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            gap: 16px;
        ">
            <div>{prev_html}</div>
            <div>{next_html}</div>
        </div>
    </div>
    """
    return HTML(html)
