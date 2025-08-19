# Contains all display related utils
from IPython.display import display, HTML

def header(title: str, keywords: list[str] = []):
    """
    Display header for notebook.

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
    if len(keywords) == 0:
        keywords_str = ""
    else:
        keywords_str = "; ".join(keywords) + ";"
    
    html_code = f"""
    <div style="font-family: 'Georgia', serif; border-left: 3px solid #ccc; 
                padding-left: 12px; margin-bottom: 1em;">
        <h2 style="margin: 0; color: #EF8C00; font-size: 2.4em; 
                   padding-left: 0; text-indent: 0;">
            {title}
        </h2>
        <p>
            {keywords_str}
        </p>
    </div>
    """
    display(HTML(html_code))


def calendar():
	"""
	Display calendar type date on the right side.
	Returns
	-------
	None
	"""
	from datetime import datetime
	
	now = datetime.now()
	day = now.strftime("%d")
	month = now.strftime("%b")
	year = now.strftime("%Y")
	time = now.strftime("%I:%M:%S %p")
	
	html_code = f"""
	<div style="
		display: flex;
		justify-content: flex-end;
		width: 100%;
		margin: 10px 0;
	">
		<div style="
			display: inline-block;
			font-family: 'Arial', sans-serif;
			border-radius: 8px;
			overflow: hidden;
			box-shadow: 1px 1px 6px rgba(0,0,0,0.1);
			width: 120px;
			font-size: 12px;
			text-align: center;
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
	</div>
	"""
	
	display(HTML(html_code))

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

def toc(tasks, current_task=1):
	"""
	Display a planner.
	
	Parameters
	----------
	tasks: list[str]
		List of task names
	current_task: int
		Current task (1-based)

	Returns
	-------
	None
	"""
	html_parts = []
	current_task -= 1 # To handle 0-indexing
	
	for i, task in enumerate(tasks):
		# Status based on index
		if i < current_task:
			dot_color = "#4caf50"  # green - done
			text_color = "#4caf50"
			icon = "✓"
		elif i == current_task:
			dot_color = "#ff9800"  # orange - current
			text_color = "#ff9800"
			icon = "●"
		else:
			dot_color = "#ddd"     # gray - pending
			text_color = "#999"
			icon = "○"
		
		# Add connecting line (except for last item)
		connector = ""
		if i < len(tasks) - 1:
			line_color = dot_color if i < current_task else "#ddd"
			connector = f'<div style="width:2px; height:20px; background:{line_color}; margin-left:9px; margin-top:-4px;"></div>'
		
		html_parts.append(f"""
		<div>
			<div style="display:flex; align-items:center; margin-bottom:0;">
				<div style="
					width:20px; height:20px; border-radius:50%; 
					background:{dot_color}; color:white; 
					display:flex; align-items:center; justify-content:center;
					font-size:10px; font-weight:bold;
					box-shadow: 0 2px 4px rgba(0,0,0,0.1);
				">{icon}</div>
				<div style="margin-left:10px; font:12px Arial; color:{text_color}; font-weight:500;">
					{task}
				</div>
			</div>
			{connector}
		</div>
		""")
	
	progress = int((current_task) / len(tasks) * 100) if tasks else 0
	
	html = f"""
	<div style="padding:12px; border-radius:6px; background:#f9f9f9; margin:8px 0; border-left:3px solid #667eea;">
		<div style="font:bold 16px Arial; color:#333; margin-bottom:12px;">
			📋 Table of Contents
		</div>
		<div style="font:11px Arial; color:#666; margin-bottom:8px;">
			Progress: {progress}% ({current_task}/{len(tasks)})
		</div>
		{''.join(html_parts)}
	</div>
	"""
	
	display(HTML(html))