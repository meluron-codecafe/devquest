from IPython.display import display, HTML

def hero(
    topic: str = "Untitled", 
    gitlink: str = "https://github.com/meluron-codecafe", 
    gitname: str = "meluron-codecafe",
):
    """
    Hero section to mention the topic along with link

    Args
    ----
    topic (str): The topic name to display
    gitlink (str): Link to the github page
    gitname (str): Display name for the github

    Returns
    -------
    None
    """
    display(HTML(f"""
    <div style="
        position: relative;
        display: flex; 
        align-items: center; 
        justify-content: flex-start;
        min-height: 80px;
        width: 800px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
        margin: 10px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">

        <!-- GitHub Icon + Name in top-right -->
        <a href="{gitlink}" target="_blank" style="
            position: absolute;
            top: 16px;
            right: 20px;
            display: flex;
            align-items: center;
            text-decoration: none;
            color: #333;
            font-size: 14px;
            font-weight: 500;
            gap: 6px;
        ">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" 
                 alt="GitHub" 
                 style="width: 18px; height: 18px; display: inline-block; vertical-align: middle;">
            <span style="transform: translateY(-1px); line-height: 1;">
                /{gitname}
            </span>
        </a>

        <!-- Logo + Label stacked vertically -->
        <div style="
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            margin-right: 35px;
        ">
            <a href="https://meluron-codecafe.github.io/DevQuest/">
                <img src="https://raw.githubusercontent.com/meluron/assets/refs/heads/main/logos/meluron-codecafe/DevQuest/icon_with_text.png" 
                     alt="My Logo" 
                     style="
                        width: 120px; 
                        height: 50px;
                        border-radius: 5px;
                        box-shadow: 0 3px 10px rgba(253, 138, 9, 0.3);
                     ">
            </a>
            <div style="
                font-size: 13px; 
                color: #fd8a09; 
                font-weight: bold;
                margin-top: 6px;
                text-align: center;
            ">
            </div>
        </div>

        <!-- Question Badge -->
        <div style="
            font-size: 14px; 
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; 
            padding: 8px 10px; 
            border-radius: 5px; 
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
            box-shadow: 0 3px 12px rgba(102, 126, 234, 0.3);
            margin-top: -10px;
        ">
            {topic}
            
        </div>
    </div>
    """))

def h1(topic: str = "Untitled"):
    """
    Create a beautiful h1 header for tutorial sections.
    
    Args
    ----
    topic (str): The subtopic name to display

    Returns
    -------
    None
    """
    display(HTML(f"""
        <div style="
            margin: 25px 0 15px 0;
            padding: 0;
        ">
            <h2 style="
                font-size: 24px;
                font-weight: 600;
                color: #2c3e50;
                margin: 0;
                padding: 12px 0 8px 0;
                display: inline-block;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">▶ {topic}</h2>
        </div>
    """))

def h2(topic: str = "Untitled"):
    """
    Create a beautiful h2 header for tutorial sections.
    
    Args
    ----
    topic (str): The section name to display

    Returns
    -------
    None
    """
    display(HTML(f"""
        <div style="
            margin: 25px 0 15px 0;
            padding: 0;
        ">
            <h3 style="
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                margin: 0;
                padding: 12px 0 8px 0;
                display: inline-block;
                border-bottom: 3px solid #667eea;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">{topic}</h3>
        </div>
    """))