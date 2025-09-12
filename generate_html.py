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
    - Bulb icon to toggle between themes (defaults to dark).
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
    
    .theme-toggle:hover {
      background: #3a3a3a;
      transform: scale(1.1);
    }
    
    body.light-mode .theme-toggle {
      background: #f5f5f5;
      color: #333;
      border-color: #ddd;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    body.light-mode .theme-toggle:hover {
      background: #e0e0e0;
    }
    
    /* ======= DARK THEME (Default) ======= */
    body {
      background-color: #1e1e1e !important;
      color: #d4d4d4 !important;
      transition: background-color 0.3s ease, color 0.3s ease;
    }
    .jp-Notebook, .jp-Cell, .jp-InputArea, .jp-OutputArea {
      background: #1e1e1e !important;
      color: #d4d4d4 !important;
      transition: background-color 0.3s ease, color 0.3s ease;
    }
    .jp-RenderedHTMLCommon, .jp-OutputArea-output {
      color: #d4d4d4 !important;
      transition: color 0.3s ease;
    }
    
    /* Links */
    a:link, a:visited {
      color: #4aa3ff !important;
    }
    a:hover, a:active {
      color: #82c7ff !important;
    }
    
    /* Blockquotes */
    blockquote {
      border-left: 4px solid #569cd6;
      padding-left: 12px;
      margin-left: 0;
      font-style: italic;
      color: #cccccc;
      background: #2a2a2a;
      transition: all 0.3s ease;
    }
    
    /* Tables */
    table {
      border-collapse: collapse;
      width: 100%;
      background: #1e1e1e;
      color: #d4d4d4;
      transition: all 0.3s ease;
    }
    table, th, td {
      border: 1px solid #444;
      padding: 6px 10px;
      transition: border-color 0.3s ease;
    }
    th {
      background: #2d2d2d;
      font-weight: bold;
      transition: background-color 0.3s ease;
    }
    tr:nth-child(even) {
      background: #242424;
      transition: background-color 0.3s ease;
    }
    
    /* ======= LIGHT MODE OVERRIDES ======= */
    body.light-mode {
      background-color: #ffffff !important;
      color: #333333 !important;
    }
    body.light-mode .jp-Notebook, 
    body.light-mode .jp-Cell, 
    body.light-mode .jp-InputArea, 
    body.light-mode .jp-OutputArea {
      background: #ffffff !important;
      color: #333333 !important;
    }
    body.light-mode .jp-RenderedHTMLCommon, 
    body.light-mode .jp-OutputArea-output {
      color: #333333 !important;
    }
    
    /* Light mode links */
    body.light-mode a:link, 
    body.light-mode a:visited {
      color: #0066cc !important;
    }
    body.light-mode a:hover, 
    body.light-mode a:active {
      color: #004499 !important;
    }
    
    /* Light mode blockquotes */
    body.light-mode blockquote {
      border-left: 4px solid #0066cc;
      color: #555;
      background: #f5f5f5;
    }
    
    /* Light mode tables */
    body.light-mode table {
      background: #ffffff;
      color: #333333;
    }
    body.light-mode table, 
    body.light-mode th, 
    body.light-mode td {
      border: 1px solid #ddd;
    }
    body.light-mode th {
      background: #f5f5f5;
    }
    body.light-mode tr:nth-child(even) {
      background: #f9f9f9;
    }
    
    /* ======= CODE CELLS ======= */
    div.highlight {
      position: relative;
      overflow-x: auto;
      padding: 0.2px 0.2px;
      transition: background-color 0.3s ease;
    }
    
    pre, code {
      background-color: #1e1e1e !important;
      border: none !important;
      color: #d4d4d4 !important;
      font-family: "Fira Code", Consolas, monospace !important;
      font-size: 13px;
      line-height: 1.5;
      white-space: pre;
      display: block;
      overflow-x: auto;
      max-width: 100%;
      transition: all 0.3s ease;
    }
    
    /* Light mode code */
    body.light-mode pre, 
    body.light-mode code {
      background-color: #f8f8f8 !important;
      color: #333333 !important;
    }
    
    /* Copy Button */
    .copy-btn {
      position: absolute;
      top: 6px;
      right: 8px;
      background: #2d2d2d;
      color: #d4d4d4;
      border: 1px solid #444;
      border-radius: 6px;
      font-size: 11px;
      padding: 2px 6px;
      cursor: pointer;
      opacity: 0.6;
      z-index: 5;
      transition: all 0.3s ease;
    }
    .copy-btn:hover {
      opacity: 1;
      background: #3a3a3a;
    }
    
    /* Light mode copy button */
    body.light-mode .copy-btn {
      background: #e0e0e0;
      color: #333;
      border-color: #ccc;
    }
    body.light-mode .copy-btn:hover {
      background: #d0d0d0;
    }
    
    /* ======= DARK MODE SYNTAX COLORS ======= */
    .k, .kp, .kt, .kc, .kd, .kn { color: #c586c0 !important; }
    .nf, .nc, .nn { color: #4fc1ff !important; }
    .n { color: #ffffff !important; }
    .s, .sb, .sc, .sd, .s1, .s2, .sa, .se { color: #6a9955 !important; }
    .m, .mf, .mi, .il { color: #d19a66 !important; }
    .c, .cm, .cpf { color: #6a9955 !important; font-style: italic !important; }
    .o, .p { color: #d4d4d4 !important; }
    
    /* ======= LIGHT MODE SYNTAX COLORS ======= */
    body.light-mode .k, body.light-mode .kp, body.light-mode .kt, 
    body.light-mode .kc, body.light-mode .kd, body.light-mode .kn { 
      color: #8B008B !important; 
    }
    body.light-mode .nf, body.light-mode .nc, body.light-mode .nn { 
      color: #0000FF !important; 
    }
    body.light-mode .n { color: #000000 !important; }
    body.light-mode .s, body.light-mode .sb, body.light-mode .sc, 
    body.light-mode .sd, body.light-mode .s1, body.light-mode .s2, 
    body.light-mode .sa, body.light-mode .se { 
      color: #008000 !important; 
    }
    body.light-mode .m, body.light-mode .mf, body.light-mode .mi, 
    body.light-mode .il { 
      color: #FF4500 !important; 
    }
    body.light-mode .c, body.light-mode .cm, body.light-mode .cpf { 
      color: #008000 !important; 
      font-style: italic !important; 
    }
    body.light-mode .o, body.light-mode .p { color: #333333 !important; }
    </style>
    """
  
    toggle_js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
      // Create theme toggle button
      var toggleBtn = document.createElement("button");
      toggleBtn.className = "theme-toggle";
      toggleBtn.innerHTML = "💡";
      toggleBtn.title = "Toggle light/dark mode";
      
      // Default to dark mode
      var isDarkMode = true;
      
      toggleBtn.addEventListener("click", function() {
        isDarkMode = !isDarkMode;
        if (isDarkMode) {
          document.body.classList.remove("light-mode");
          toggleBtn.innerHTML = "💡";
          toggleBtn.title = "Switch to light mode";
        } else {
          document.body.classList.add("light-mode");
          toggleBtn.innerHTML = "🌙";
          toggleBtn.title = "Switch to dark mode";
        }
      });
      
      document.body.appendChild(toggleBtn);
      
      // Add copy buttons to code blocks
      document.querySelectorAll("div.highlight").forEach(function(block) {
        var btn = document.createElement("button");
        btn.innerHTML = "Copy code";
        btn.className = "copy-btn";
        btn.title = "Copy code";
    
        btn.addEventListener("click", function(event) {
          event.stopPropagation();
    
          var codeBlock = block.querySelector("code") || block.querySelector("pre");
          if (!codeBlock) return;
    
          var code = codeBlock.innerText;
    
          navigator.clipboard.writeText(code).then(() => {
            btn.innerHTML = "Copied!";
            btn.style.color = isDarkMode ? "#ffffff" : "#000000";
            setTimeout(() => { 
              btn.innerHTML = "Copy code"; 
              btn.style.color = isDarkMode ? "#d4d4d4" : "#333333"; 
            }, 1500);
          });
        });
    
        block.appendChild(btn);
      });
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
    """
    Extract category, topic, subtopics, and number from filename like:
    CATEGORY-TOPIC_NAME-SUBTOPICS-NUMBER.ipynb
    """
    pattern = re.compile(
        r"^(?P<category>[^-]+)-(?P<topic>[^-]*)-(?P<number>\d+)\.ipynb$"
    )
    match = pattern.match(file_path.name)
    if not match:
        return None, None, None
    
    category = match.group("category")
    topic = match.group("topic").replace("_", " ")
    
    number = match.group("number")
    return category, topic, number

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .ipynb to HTML, strip hidden code, and generate tutorials.csv")
    parser.add_argument("-i", "--input", type=str, required=False, help="Path to .ipynb file")
    parser.add_argument("--all", action="store_true", help="Convert all notebooks to HTMLs")
    args = parser.parse_args()
    
    root_dir = Path(__file__).parent
    
    if args.all:
        csv_rows = []
        notebooks_dir = root_dir / "notebooks"
        # Get all .ipynb paths and sort them
        notebooks = sorted(notebooks_dir.glob("*.ipynb"))
        
        for notebook in notebooks:
            tags = export_clean_html(notebook)
            category, topic, number = extract_info_from_filename(notebook)
            if category:
                csv_rows.append([
                    category,
                    topic,
                    tags,
                    number.zfill(2),
                    notebook.name,
                    f"{notebook.stem}.html",
                ])
        
        # Save CSV with correct header
        csv_file = root_dir / "tutorials.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["category", "topic", "tags", "number", "notebook", "html"])
            writer.writerows(csv_rows)
            
        print(f"✅ Saved CSV to {csv_file}")
        
    else:
        if not args.input:
            parser.error("argument -i/--input is required unless --all is specified")
            
        notebook_path = Path(args.input)
        keywords = export_clean_html(notebook_path)
        
        category, topic, number = extract_info_from_filename(notebook_path)
        if not category:
            print(f"⚠️ Skipped {notebook_path} (missing category info)")
            exit()
            
        new_row = [
            category,
            topic,
            keywords,
            number.zfill(2),
            notebook_path.name,
            f"{notebook_path.stem}.html",
        ]
        
        csv_file = root_dir / "tutorials.csv"
        
        # Load existing CSV rows (if file exists)
        if csv_file.exists():
            with open(csv_file, mode="r", newline="", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                header, rows = reader[0], reader[1:]
        else:
            header, rows = ["category", "topic", "tags", "number", "notebook", "html"], []
            
        # Update or append row
        updated = False
        for idx, row in enumerate(rows):
            if row[4] == new_row[4]:  # match by notebook filename
                rows[idx] = new_row
                updated = True
                break
        if not updated:
            rows.append(new_row)
            
        # Sort again
        rows.sort(key=lambda x: x[4])
        
        # Save back to CSV
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
            
        print(f"✅ {'Updated' if updated else 'Added'} row for {notebook_path.name} in {csv_file}")
      