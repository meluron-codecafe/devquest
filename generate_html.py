#!/usr/bin/env python3

from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
import nbformat
from pathlib import Path
import argparse
import os
import re
import csv

root_dir = Path(__file__).parent.resolve()

def convert_to_html(notebook_path: Path) -> str:
    """
    Convert .ipynb to .html using nbformat.

    Parameters
    ----------
    notebook_path: Path
    """
    notebook = nbformat.read(notebook_path, as_version=4)
    exporter = HTMLExporter()
    body, _ = exporter.from_notebook_node(notebook)
    return body

def strip_hidden_code_cells_and_tag_keywords(html_content: str) -> (str, int, str):
    """
    - Remove cells with #hide at the start.
    - Add 'tags' class to the first <p> in the first markdown cell.
    - Extract the keywords text.
    Returns: (cleaned_html, removed_count, keywords_text)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    removed = 0
    
    # Remove hidden code cells
    for input_block in soup.select('.jp-InputArea'):
        pre = input_block.find('pre')
        if pre and pre.text.strip().startswith('#hide'):
            input_block.decompose()
            removed += 1
            
    # Add class to first <p> in first markdown cell and extract keywords
    tags = ""
    first_markdown = soup.select_one('.jp-RenderedHTMLCommon p')
    if first_markdown:
        first_markdown['class'] = first_markdown.get('class', []) + ['keywords']
        tags = first_markdown.get_text(strip=True)
        
    return str(soup), removed, tags
  
def inject_css(html: str) -> str:
  """
  Apply a toggleable dark/light theme to nbconvert HTML output.
  - Code cells: VSCode Dark+ style with custom colors + Copy button.
  - Markdown/output cells: simple dark/light mode toggle.
  - Right Vertical Timeline TOC: Vertical progress timeline on the right.
  - Hover for 3s on timeline to see all headings (numbered).
  - Bulb icon to toggle between themes (defaults to dark).
  - Report Issue button to submit feedback on GitHub.
  """
  theme_css = """
    <style>
    /* ======= THEME TOGGLE BUTTON ======= */
    .theme-toggle {
      position: fixed;
      top: 20px;
      right: 20px;
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
      font-size: 20px;
      transition: all 0.3s ease;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .theme-toggle:hover { background: #3a3a3a; transform: scale(1.1); }
    body.light-mode .theme-toggle { background: #f5f5f5; color: #333; border-color: #ddd; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    body.light-mode .theme-toggle:hover { background: #e0e0e0; }
    
    /* ======= REPORT ISSUE BUTTON (SAME STYLE AS THEME TOGGLE) ======= */
    .report-issue-btn {
      position: fixed;
      top: 20px;
      right: 80px;
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
      font-size: 20px;
      transition: all 0.3s ease;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
      text-decoration: none;
    }
    .report-issue-btn:hover { background: #3a3a3a; transform: scale(1.1); }
    body.light-mode .report-issue-btn { background: #f5f5f5; color: #333; border-color: #ddd; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    body.light-mode .report-issue-btn:hover { background: #e0e0e0; }
    
    /* ======= CONTENT SPACING FOR TIMELINE ======= */
    body {
      margin-right: 80px !important; /* Space for timeline */
      transition: margin-right 0.3s ease;
    }
    
    .jp-Notebook {
      max-width: calc(100% - 80px) !important; /* Ensure notebook doesn't extend into timeline area */
      margin-right: 0 !important;
    }
    
    .jp-Cell {
      margin-right: 20px !important; /* Additional margin for cells */
    }
    
    /* ======= VERTICAL TIMELINE TOC (RIGHT) ======= */
    #timeline-nav {
      position: fixed !important; top: 50% !important; right: 25px !important; transform: translateY(-50%) !important;
      background: rgba(20, 20, 20, 0.95) !important; backdrop-filter: blur(20px) !important;
      border-radius: 25px !important; padding: 20px 12px !important; z-index: 999 !important;
      transition: all 0.3s ease !important; border: 1px solid rgba(255,255,255,0.1) !important;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important; display: flex !important; flex-direction: column !important;
      align-items: center !important; gap: 8px !important;
    }
  
    .timeline-dot {
      width: 20px;
      height: 20px;
      background: #374151;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 444;
      color: red !important; /* default for dark mode */
      transition: all 0.3s ease;
      text-decoration: none;
      cursor: pointer;
      flex-shrink: 0;
      margin: -8px;
    }
    
    .timeline-dot,
    .timeline-dot:link,
    .timeline-dot:visited,
    .timeline-dot:hover,
    .timeline-dot:active {
      color: white !important;  /* dark mode */
      text-decoration: none;    /* remove underline */
    }
    
    body.light-mode .timeline-dot,
    body.light-mode .timeline-dot:link,
    body.light-mode .timeline-dot:visited,
    body.light-mode .timeline-dot:hover,
    body.light-mode .timeline-dot:active {
      color: white !important;  /* light mode */
    }
      
    .timeline-dot.completed { background: #228B22; color: black; }
    .timeline-dot.current { background: #fd8a09; color: black; }
    .timeline-dot.future { background: #374151; color: white; }
    .timeline-dot:hover { transform: scale(1.4) !important; }
    .timeline-dot.completed:hover { box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.3) !important; }
    .timeline-dot.current:hover { box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.3) !important; }
    .timeline-dot.future:hover { box-shadow: 0 0 0 4px rgba(55, 65, 81, 0.3) !important; }
    body.light-mode .timeline-dot { color: black !important; }
  
    .timeline-line { width: 2px; height: 25px; background: #374151; transition: all 0.3s ease; flex-shrink: 0; }
    .timeline-line.completed { background: #4ade80; }

    /* Timeline Tooltip (for single dots) */
    #timeline-tooltip {
      position: fixed; background: rgba(0,0,0,0.9); color: white; padding: 8px 12px; border-radius: 8px;
      font-size: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; pointer-events: none;
      z-index: 1001; opacity: 0; transition: all 0.2s ease; white-space: nowrap;
    }
    .tooltip-text { opacity: 0.9; font-size: 11px; font-weight: 600; }
  
    /* Timeline Full List */
    #timeline-full-list {
      position: fixed; background: rgba(20,20,20,0.95); color: white; padding: 12px 16px; border-radius: 12px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; backdrop-filter: blur(20px);
      z-index: 1002; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
      max-height: 80vh; overflow-y: auto; border: 1px solid rgba(255,255,255,0.1);
    }
    #timeline-full-list ul { list-style: none; padding: 0; margin: 0; font-size: 11px; }
    #timeline-full-list li { padding: 4px 0; opacity: 0.8; white-space: nowrap; }
  
    /* Light mode timeline styles */
    body.light-mode #timeline-nav { background: rgba(255,255,255,0.95) !important; border-color: rgba(0,0,0,0.1) !important; box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important; }
    body.light-mode .timeline-dot.future { background: #d1d5db; }
    body.light-mode .timeline-line { background: #d1d5db; }
    body.light-mode #timeline-tooltip { background: rgba(255,255,255,0.95); color: #333; border: 1px solid rgba(0,0,0,0.1); }
    body.light-mode #timeline-full-list { background: rgba(255,255,255,0.95); color: #333; border: 1px solid rgba(0,0,0,0.1); }
  
    /* ======= GENERAL DARK/LIGHT STYLES ======= */
    body { background-color: #1e1e1e !important; color: #d4d4d4 !important; transition: background-color 0.3s ease, color 0.3s ease; }
    .jp-Notebook, .jp-Cell, .jp-InputArea, .jp-OutputArea { background: #1e1e1e !important; color: #d4d4d4 !important; transition: background-color 0.3s ease, color 0.3s ease; }
    .jp-RenderedHTMLCommon, .jp-OutputArea-output { color: #d4d4d4 !important; transition: color 0.3s ease; }
    html { scroll-behavior: smooth; } h1, h2, h3, h4, h5, h6 { scroll-margin-top: 20px; }
    a:link, a:visited { color: #4aa3ff !important; } a:hover, a:active { color: #82c7ff !important; }
    blockquote { border-left: 4px solid #569cd6; padding-left: 12px; margin-left: 0; font-style: italic; color: #cccccc; background: #2a2a2a; transition: all 0.3s ease; }
    table { border-collapse: collapse; width: 100%; background: #1e1e1e; color: #d4d4d4; transition: all 0.3s ease; }
    table, th, td { border: 1px solid #444; padding: 6px 10px; transition: border-color 0.3s ease; }
    th { background: #2d2d2d; font-weight: bold; transition: background-color 0.3s ease; }
    tr:nth-child(even) { background: #242424; transition: background-color 0.3s ease; }
    body.light-mode { background-color: #ffffff !important; color: #333333 !important; }
    body.light-mode .jp-Notebook, body.light-mode .jp-Cell, body.light-mode .jp-InputArea, body.light-mode .jp-OutputArea { background: #ffffff !important; color: #333333 !important; }
    body.light-mode .jp-RenderedHTMLCommon, body.light-mode .jp-OutputArea-output { color: #333333 !important; }
    body.light-mode a:link, body.light-mode a:visited { color: #0066cc !important; }
    body.light-mode a:hover, body.light-mode a:active { color: #004499 !important; }
    body.light-mode blockquote { border-left: 4px solid #0066cc; color: #555; background: #f5f5f5; }
    body.light-mode table { background: #ffffff; color: #333333; }
    body.light-mode table, body.light-mode th, body.light-mode td { border: 1px solid #ddd; }
    body.light-mode th { background: #f5f5f5; }
    body.light-mode tr:nth-child(even) { background: #f9f9f9; }
    div.highlight { position: relative; overflow-x: auto; padding: 0.2px 0.2px; transition: background-color 0.3s ease; }
    pre, code { background-color: #1e1e1e !important; border: none !important; color: #d4d4d4 !important; font-family: "Fira Code", Consolas, monospace !important; font-size: 13px; line-height: 1.5; white-space: pre; display: block; overflow-x: auto; max-width: 100%; transition: all 0.3s ease; }
    body.light-mode pre, body.light-mode code { background-color: #f8f8f8 !important; color: #333333 !important; }
    .copy-btn { position: absolute; top: 6px; right: 8px; background: #2d2d2d; color: #d4d4d4; border: 1px solid #444; border-radius: 6px; font-size: 11px; padding: 2px 6px; cursor: pointer; opacity: 0.6; z-index: 5; transition: all 0.3s ease; }
    .copy-btn:hover { opacity: 1; background: #3a3a3a; }
    body.light-mode .copy-btn { background: #e0e0e0; color: #333; border-color: #ccc; }
    body.light-mode .copy-btn:hover { background: #d0d0d0; }
    .k, .kp, .kt, .kc, .kd, .kn { color: #c586c0 !important; } .nf, .nc, .nn { color: #4fc1ff !important; } .n { color: #ffffff !important; } .s, .sb, .sc, .sd, .s1, .s2, .sa, .se { color: #6a9955 !important; } .m, .mf, .mi, .il { color: #d19a66 !important; } .c, .cm, .cpf { color: #6a9955 !important; font-style: italic !important; } .o, .p { color: #d4d4d4 !important; }
    body.light-mode .k, body.light-mode .kp, body.light-mode .kt, body.light-mode .kc, body.light-mode .kd, body.light-mode .kn { color: #8B008B !important; } body.light-mode .nf, body.light-mode .nc, body.light-mode .nn { color: #0000FF !important; } body.light-mode .n { color: #000000 !important; } body.light-mode .s, body.light-mode .sb, body.light-mode .sc, body.light-mode .sd, body.light-mode .s1, body.light-mode .s2, body.light-mode .sa, body.light-mode .se { color: #008000 !important; } body.light-mode .m, body.light-mode .mf, body.light-mode .mi, body.light-mode .il { color: #FF4500 !important; } body.light-mode .c, body.light-mode .cm, body.light-mode .cpf { color: #008000 !important; font-style: italic !important; } body.light-mode .o, body.light-mode .p { color: #333333 !important; }
    
    /* ======= MOBILE RESPONSIVE ======= */
    @media (max-width: 768px) { 
      body {
        margin-right: 60px !important; /* Less space on tablets */
      }
      
      .jp-Notebook {
        max-width: calc(100% - 60px) !important;
      }
      
      .jp-Cell {
        margin-right: 10px !important; /* Less margin on tablets */
      }
      
      #timeline-nav { 
        right: 10px !important; 
        padding: 15px 8px !important; 
        gap: 6px !important; 
      } 
      .timeline-line { height: 15px !important; } 
      .theme-toggle { top: 10px; right: 10px; width: 40px; height: 40px; font-size: 16px; } 
      .report-issue-btn { 
        top: 10px; 
        right: 60px; 
        width: 40px;
        height: 40px;
        font-size: 16px;
      }
    }
    
    @media (max-width: 480px) { 
      body {
        margin-right: 0 !important; /* No margin on phones since timeline is hidden */
      }
      
      .jp-Notebook {
        max-width: 100% !important;
      }
      
      .jp-Cell {
        margin-right: 0 !important;
      }
      
      .theme-toggle { top: 10px; right: 10px; }
      .report-issue-btn { 
        top: 60px; 
        right: 10px; 
        width: 40px;
        height: 40px;
        font-size: 16px;
      }
    }
    </style>
    """
  
  toggle_js = """
  <script>
  document.addEventListener("DOMContentLoaded", function() {
    // Theme toggle button
    var themeToggle = document.createElement("button");
    themeToggle.className = "theme-toggle";
    themeToggle.innerHTML = "💡";
    themeToggle.title = "Toggle light/dark mode";
    var isDarkMode = true;
    themeToggle.addEventListener("click", function() {
      isDarkMode = !isDarkMode;
      document.body.classList.toggle("light-mode", !isDarkMode);
      themeToggle.innerHTML = isDarkMode ? "💡" : "🌙";
      themeToggle.title = isDarkMode ? "Switch to light mode" : "Switch to dark mode";
    });
    document.body.appendChild(themeToggle);

    // Report issue button - SAME STYLE AS THEME TOGGLE
    var reportIssueBtn = document.createElement("a");
    reportIssueBtn.className = "report-issue-btn";
    reportIssueBtn.innerHTML = "⚠️";
    reportIssueBtn.title = "Report an issue in this notebook";
    reportIssueBtn.target = "_blank";
    reportIssueBtn.rel = "noopener noreferrer";
    
    // Construct GitHub URL
    var issueTitle = "[Tutorial Content Issue]";
    var issueBody = encodeURIComponent("Tutorial Page: " + window.location.href + "\\n\\nMention Issue: \\n");
    reportIssueBtn.href = "https://github.com/meluron-codecafe/DevQuest/issues/new?assignees=ankit0anand0&labels=tutorials&projects=&template=&title=" + issueTitle + "&body=" + issueBody;
    
    document.body.appendChild(reportIssueBtn);

    var timelineNav = document.createElement("div");
    timelineNav.id = "timeline-nav";
    document.body.appendChild(timelineNav);

    var tooltip = document.createElement("div");
    tooltip.id = "timeline-tooltip";
    document.body.appendChild(tooltip);

    var fullList = document.createElement("div");
    fullList.id = "timeline-full-list";
    document.body.appendChild(fullList);

    var headings = [];

    function generateTimeline() {
      headings = Array.from(document.querySelectorAll("h2"));
      if (headings.length === 0) return;

      headings.forEach(function(heading, index) {
        if (!heading.id) heading.id = "heading-" + index;
        if (index > 0) {
          var line = document.createElement("div");
          line.className = "timeline-line";
          timelineNav.appendChild(line);
        }
        var dot = document.createElement("a");
        dot.className = "timeline-dot future";
        dot.href = "#" + heading.id;
        dot.textContent = index + 1;  // number inside circle

        dot.addEventListener("click", (e) => {
          e.preventDefault();
          heading.scrollIntoView({ behavior: "smooth" });
        });

        function cleanHeadingText(heading) {
          let text = heading.textContent.trim();
          // Remove pilcrow or any trailing symbols typically added by nbconvert
          text = text.replace(/[\u00B6]/g, ''); 
          return text;
        }

        let hoverTimeout;
        dot.addEventListener("mouseenter", () => {
          // Show single tooltip
          var text = cleanHeadingText(heading);
          if (text.length > 40) text = text.substring(0, 40) + "...";
          var rect = dot.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tooltip-text">' + text + '</div>';
          tooltip.style.top = (rect.top + rect.height / 2 - tooltip.offsetHeight / 2) + 'px';
          tooltip.style.left = (rect.left - tooltip.offsetWidth - 10) + 'px';
          tooltip.style.opacity = '1';

          // Show full list after 3s
          hoverTimeout = setTimeout(() => {
            fullList.innerHTML = "<ul>" + headings.map((h,i) => "<li>" + (i+1) + ". " + cleanHeadingText(h) + "</li>").join("") + "</ul>";
            var navRect = timelineNav.getBoundingClientRect();
            fullList.style.top = navRect.top + 'px';
            fullList.style.left = (navRect.left - fullList.offsetWidth - 15) + 'px';
            fullList.style.opacity = '1';
          }, 1500);
        });

        dot.addEventListener("mouseleave", () => {
          clearTimeout(hoverTimeout);
          tooltip.style.opacity = '0';
          fullList.style.opacity = '0';
        });

        timelineNav.appendChild(dot);
      });

      updateTimeline();
    }

    function updateTimeline() {
      if (headings.length === 0) return;
      var scrollPos = window.scrollY + (window.innerHeight / 2);
      var currentIndex = -1;
      for (var i = 0; i < headings.length; i++) { if (headings[i].offsetTop <= scrollPos) currentIndex = i; }

      timelineNav.querySelectorAll(".timeline-dot").forEach((dot, index) => {
        dot.className = "timeline-dot";
        if (index < currentIndex) dot.classList.add("completed");
        else if (index === currentIndex) dot.classList.add("current");
        else dot.classList.add("future");
      });

      timelineNav.querySelectorAll(".timeline-line").forEach((line, index) => {
        line.classList.toggle("completed", index < currentIndex);
      });
    }

    var scrollTimeout;
    window.addEventListener("scroll", () => { clearTimeout(scrollTimeout); scrollTimeout = setTimeout(updateTimeline, 50); });

    document.querySelectorAll("div.highlight").forEach(block => {
      var btn = document.createElement("button");
      btn.innerHTML = "Copy"; btn.className = "copy-btn"; btn.title = "Copy code";
      btn.addEventListener("click", e => {
        e.stopPropagation();
        var code = block.querySelector("pre, code").innerText;
        navigator.clipboard.writeText(code).then(() => {
          btn.innerHTML = "Copied!";
          setTimeout(() => { btn.innerHTML = "Copy"; }, 1500);
        });
      });
      block.appendChild(btn);
    });

    generateTimeline();
  });
  </script>
  """
  
  return html.replace("</body>", theme_css + toggle_js + "\n</body>")

def export_clean_html(ipynb_path: Path):
    html_output_dir = root_dir / "htmls"
    html_output_dir.mkdir(parents=True, exist_ok=True)
    output_path = html_output_dir / f"{ipynb_path.stem}.html"
    
    html = convert_to_html(ipynb_path)
    cleaned_html, removed, tags = strip_hidden_code_cells_and_tag_keywords(html)
    cleaned_html = inject_css(cleaned_html)  # add additional css
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_html)
        
    print(f"{output_path.name} ✅\n--->#hide: {removed} || Tags: {tags}\n")
    return tags

def format_topic(topic: str) -> str:
    """Capitalize first letter of each word, splitting by underscore."""
    return " ".join(word.capitalize() for word in topic.split("_"))

def extract_info_from_filename(file_path: Path):
  pattern = re.compile(r"^(?P<category>[^-]+)-(?P<topic>.+)\.ipynb$")
  match = pattern.match(file_path.name)
  if not match:
    return None, None
  category = match.group("category")
  topic = match.group("topic").replace("_", " ")
  return category, topic

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Convert .ipynb to HTML and generate tutorials.csv")
  parser.add_argument("-i", "--input", type=str, help="Path to .ipynb file")
  parser.add_argument("--all", action="store_true", help="Convert all notebooks")
  args = parser.parse_args()
  
  root_dir = Path(__file__).parent
  csv_file = root_dir / "tutorials.csv"
  
  if args.all:
    notebooks_dir = root_dir / "notebooks"
    notebooks = sorted(notebooks_dir.glob("*.ipynb"))
    csv_rows = []
    
    for notebook in notebooks:
      tags = export_clean_html(notebook)
      category, topic = extract_info_from_filename(notebook)
      if category:
        csv_rows.append([category, topic, tags, f"{notebook.stem}.html"])
        
    # Write CSV
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow(["category", "topic", "tags", "html"])
      writer.writerows(csv_rows)
      
    print(f"✅ Saved CSV to {csv_file}")
    
  else:
    if not args.input:
      parser.error("argument -i/--input is required unless --all is specified")
    notebook_path = Path(args.input)
    tags = export_clean_html(notebook_path)
    category, topic = extract_info_from_filename(notebook_path)
    
    if not category:
      print(f"⚠️ Skipped {notebook_path} (missing category info)")
      exit()
      
    new_row = [category, topic, tags, f"{notebook_path.stem}.html"]
    
    # Load existing rows if CSV exists
    if csv_file.exists():
      with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header, rows = reader[0], reader[1:]
    else:
      header, rows = ["category", "topic", "tags", "html"], []
      
    # Update or append
    updated = False
    for idx, row in enumerate(rows):
      if row[3] == new_row[3]:  # match by HTML filename
        rows[idx] = new_row
        updated = True
        break
    if not updated:
      rows.append(new_row)
      
    # Sort by topic
    rows.sort(key=lambda x: x[1].lower())
    
    # Save CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow(header)
      writer.writerows(rows)
      
    print(f"✅ {'Updated' if updated else 'Added'} row for {notebook_path.name} in {csv_file}")
    