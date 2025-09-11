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
    Apply a static dark theme to nbconvert HTML output.
    - Code cells: VSCode Dark+ style with custom colors + Copy button.
    - Markdown/output cells: simple dark mode.
    """
    dark_css = """
    <style>
    /* ======= DARK THEME (Markdown, Outputs) ======= */
    body {
      background-color: #1e1e1e !important;
      color: #d4d4d4 !important;
    }
    .jp-Notebook, .jp-Cell, .jp-InputArea, .jp-OutputArea {
      background: #1e1e1e !important;
      color: #d4d4d4 !important;
    }
    .jp-RenderedHTMLCommon, .jp-OutputArea-output {
      color: #d4d4d4 !important;
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
    }
    
    /* Tables */
    table {
      border-collapse: collapse;
      width: 100%;
      background: #1e1e1e;
      color: #d4d4d4;
    }
    table, th, td {
      border: 1px solid #444;
      padding: 6px 10px;
    }
    th {
      background: #2d2d2d;
      font-weight: bold;
    }
    tr:nth-child(even) {
      background: #242424;
    }
    
    /* ======= CODE CELLS ======= */
    div.highlight {
      position: relative;   /* container relative for copy btn */
      overflow-x: auto;     /* enable horizontal scroll */
      padding: 0.2px 0.2px;      /* inner padding around code */
    }
    pre, code {
      background-color: #1e1e1e !important;
      border: none !important;
      color: #d4d4d4 !important;
      font-family: "Fira Code", Consolas, monospace !important;
      font-size: 13px;
      line-height: 1.5;
      white-space: pre;     /* preserve spacing, no wrapping */
      display: block;       /* ensure block for scrolling */
      overflow-x: auto;     /* horizontal scrolling if needed */
      max-width: 100%;      /* don’t overflow container */
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
      transition: opacity 0.2s ease-in-out, color 0.2s;
    }
    .copy-btn:hover {
      opacity: 1;
      background: #3a3a3a;
    }
    
    /* ======= SYNTAX COLORS ======= */
    .k, .kp, .kt, .kc, .kd, .kn { color: #c586c0 !important; } /* Keywords */
    .nf, .nc, .nn { color: #4fc1ff !important; }               /* Functions */
    .n { color: #ffffff !important; }                          /* Variables */
    .s, .sb, .sc, .sd, .s1, .s2, .sa, .se { color: #6a9955 !important; } /* Strings */
    .m, .mf, .mi, .il { color: #d19a66 !important; }           /* Numbers */
    .c, .cm, .cpf { color: #6a9955 !important; font-style: italic !important; } /* Comments */
    .o, .p { color: #d4d4d4 !important; }                      /* Operators */
    </style>
    """
  
    copy_js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
      document.querySelectorAll("div.highlight").forEach(function(block) {
        var btn = document.createElement("button");
        btn.innerHTML = "Copy code";
        btn.className = "copy-btn";
        btn.title = "Copy code";
    
        btn.addEventListener("click", function(event) {
          event.stopPropagation();
    
          // Prefer <code>, fallback to <pre>
          var codeBlock = block.querySelector("code") || block.querySelector("pre");
          if (!codeBlock) return;
    
          var code = codeBlock.innerText;
    
          navigator.clipboard.writeText(code).then(() => {
            btn.innerHTML = "Copied!";
            btn.style.color = "#ffffff";
            setTimeout(() => { 
              btn.innerHTML = "Copy code"; 
              btn.style.color = "#d4d4d4"; 
            }, 1500);
          });
        });
    
        block.appendChild(btn);
      });
    });
    </script>
    """
  
    return html.replace("</body>", dark_css + copy_js + "\n</body>")

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
      