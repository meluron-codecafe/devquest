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
    - Code cells: VSCode Dark+ style with custom colors + Copy button + Jupyter-style collapsible functionality.
    - Markdown/output cells: simple dark/light mode toggle.
    - Right Vertical Timeline TOC: Vertical progress timeline on the right.
    - Hover for 3s on timeline to see all headings (numbered).
    - Button container with code toggle, theme toggle button, report issue button, and aligned download button.
    - Collapsible code cells: Show first line + expand icon, just like Jupyter notebook environment.
    - Code visibility toggle: Hide/show all code cells while keeping outputs.
    - Uses SVG icons for consistent cross-device rendering.
    """
    theme_css = """
    <style>
    /* ======= CSS CUSTOM PROPERTIES ======= */
    :root {
        --text-color: #d4d4d4;
        --bg-color: #1e1e1e;
        --button-size: 40px;
    }
    
    body.light-mode {
        --text-color: #333333;
        --bg-color: #ffffff;
    }

    /* ======= BUTTON CONTAINER ======= */
    .button-container {
      position: fixed;
      top: 20px;
      right: 20px;
      background: rgba(45, 45, 45, 0.95);
      border: 1px solid #555;
      border-radius: 12px;
      padding: 2px;
      display: flex;
      gap: 0px;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      backdrop-filter: blur(10px);
      box-shadow: 0 2px 12px rgba(0,0,0,0.2);
      transition: all 0.3s ease;
      height: auto;
      width: auto;
    }

    .button-container:hover {
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    /* ======= BASE BUTTON RESET AND SIZING ======= */
    .code-toggle-btn,
    .theme-toggle-btn,
    .report-issue-btn,
    .download-btn {
        /* Reset all properties */
        all: unset;
        
        /* Set exact dimensions */
        width: var(--button-size) !important;
        height: var(--button-size) !important;
        min-width: var(--button-size) !important;
        min-height: var(--button-size) !important;
        max-width: var(--button-size) !important;
        max-height: var(--button-size) !important;
        
        /* Layout */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
        
        /* Positioning and spacing */
        position: relative !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
        
        /* Appearance */
        background: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        
        /* Typography */
        color: var(--text-color) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        line-height: 1 !important;
        text-align: center !important;
        text-decoration: none !important;
        vertical-align: top !important;
        
        /* Prevent any transformations */
        transform: none !important;
        scale: none !important;
        rotate: none !important;
        translate: none !important;
        
        /* Transitions */
        transition: background-color 0.2s ease !important;
        
        /* Overflow */
        overflow: hidden !important;
    }

    /* ======= SVG ICON STYLING ======= */
    .code-toggle-btn svg,
    .theme-toggle-btn svg,
    .report-issue-btn svg,
    .download-btn svg {
        width: 20px !important;
        height: 20px !important;
        stroke: currentColor !important;
        fill: none !important;
        transition: all 0.2s ease !important;
        flex-shrink: 0 !important;
        color: inherit !important;
    }

    /* ======= HOVER STATES ======= */
    .code-toggle-btn:hover,
    .theme-toggle-btn:hover,
    .report-issue-btn:hover,
    .download-btn:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: none !important;
        scale: none !important;
    }

    .code-toggle-btn:hover svg,
    .theme-toggle-btn:hover svg,
    .report-issue-btn:hover svg,
    .download-btn:hover svg {
        transform: none !important;
        scale: 1 !important;
    }

    /* ======= CODE TOGGLE SPECIFIC STYLES ======= */
    .code-toggle-btn {
        vertical-align: top !important;
    }
    
    /* Ensure code toggle button never changes size or position */
    .code-toggle-btn,
    .code-toggle-btn:hover,
    .code-toggle-btn:active,
    .code-toggle-btn:focus,
    .code-toggle-btn.code-hidden,
    .code-toggle-btn.code-hidden:hover,
    .code-toggle-btn.code-hidden:active,
    .code-toggle-btn.code-hidden:focus {
        width: var(--button-size) !important;
        height: var(--button-size) !important;
        transform: none !important;
        scale: none !important;
        min-width: var(--button-size) !important;
        max-width: var(--button-size) !important;
        vertical-align: top !important;
    }
    
    .code-toggle-btn.code-hidden {
        opacity: 0.6 !important;
    }

    /* ======= THEME TOGGLE SPECIFIC STYLES ======= */
    .theme-toggle-btn {
        vertical-align: top !important;
    }
    
    .theme-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) !important;
        opacity: 0;
        transition: opacity 0.3s ease;
        line-height: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .theme-icon svg {
        position: static !important;
        transform: none !important;
    }
    
    .theme-icon.active {
        opacity: 1;
    }

    /* ======= REPORT ISSUE SPECIFIC STYLES ======= */
    .report-issue-btn {
        font-weight: 700 !important;
        vertical-align: top !important;
        color: var(--text-color) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Override any link styles */
    .report-issue-btn,
    .report-issue-btn:link,
    .report-issue-btn:visited,
    .report-issue-btn:hover,
    .report-issue-btn:active {
        color: var(--text-color) !important;
        text-decoration: none !important;
    }

    /* ======= DOWNLOAD BUTTON SPECIFIC STYLES ======= */
    .download-btn {
        font-weight: 400 !important;
        vertical-align: top !important;
        color: var(--text-color) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-direction: row !important;
        gap: 0 !important;
    }
    
    /* Override any link styles */
    .download-btn,
    .download-btn:link,
    .download-btn:visited,
    .download-btn:hover,
    .download-btn:active {
        color: var(--text-color) !important;
        text-decoration: none !important;
    }

    /* ======= LIGHT MODE STYLES ======= */
    body.light-mode .button-container {
        background: rgba(255, 255, 255, 0.95);
        border-color: #ccc;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }
    
    /* Force all buttons to have correct colors in light mode */
    body.light-mode .code-toggle-btn,
    body.light-mode .theme-toggle-btn,
    body.light-mode .report-issue-btn,
    body.light-mode .download-btn {
        color: #333333 !important;
    }
    
    /* SVG colors in light mode */
    body.light-mode .code-toggle-btn svg,
    body.light-mode .theme-toggle-btn svg,
    body.light-mode .report-issue-btn svg,
    body.light-mode .download-btn svg {
        stroke: #333333 !important;
        color: #333333 !important;
    }
    
    /* Extra specific overrides for report issue button in light mode */
    body.light-mode .report-issue-btn,
    body.light-mode .report-issue-btn:link,
    body.light-mode .report-issue-btn:visited,
    body.light-mode .report-issue-btn:hover,
    body.light-mode .report-issue-btn:active,
    body.light-mode .report-issue-btn:focus {
        color: #333333 !important;
        text-decoration: none !important;
    }
    
    /* Extra specific overrides for download button in light mode */
    body.light-mode .download-btn,
    body.light-mode .download-btn:link,
    body.light-mode .download-btn:visited,
    body.light-mode .download-btn:hover,
    body.light-mode .download-btn:active,
    body.light-mode .download-btn:focus {
        color: #333333 !important;
        text-decoration: none !important;
    }
    
    body.light-mode .code-toggle-btn:hover,
    body.light-mode .theme-toggle-btn:hover,
    body.light-mode .report-issue-btn:hover,
    body.light-mode .download-btn:hover {
        background: rgba(0, 0, 0, 0.05) !important;
    }

    /* ======= CODE VISIBILITY TOGGLE ======= */
    .code-hidden .jp-Cell:has(.jp-InputArea div.highlight) .jp-InputArea {
      display: none !important;
    }
    
    .code-hidden .jp-InputArea:has(div.highlight) {
      display: none !important;
    }

    /* ======= CONTENT SPACING FOR TIMELINE ======= */
    body {
      margin-right: 80px !important;
      transition: margin-right 0.3s ease;
    }
    
    .jp-Notebook {
      max-width: calc(100% - 240px) !important;
      margin-right: 0 !important;
    }
    
    .jp-Cell {
      margin-right: 40px !important;
    }
    
    /* ======= VERTICAL TIMELINE TOC (RIGHT) ======= */
    #timeline-nav {
      position: fixed !important; 
      top: 50% !important; 
      right: 25px !important; 
      transform: translateY(-50%) !important;
      background: rgba(20, 20, 20, 0.95) !important; 
      backdrop-filter: blur(20px) !important;
      border-radius: 25px !important; 
      padding: 20px 12px !important; 
      z-index: 999 !important;
      transition: all 0.3s ease !important; 
      border: 1px solid rgba(255,255,255,0.1) !important;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important; 
      display: flex !important; 
      flex-direction: column !important;
      align-items: center !important; 
      gap: 8px !important;
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
      color: white !important;
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
      color: white !important;
      text-decoration: none;
    }
    
    body.light-mode .timeline-dot,
    body.light-mode .timeline-dot:link,
    body.light-mode .timeline-dot:visited,
    body.light-mode .timeline-dot:hover,
    body.light-mode .timeline-dot:active {
      color: white !important;
    }
      
    .timeline-dot.completed { background: #228B22; color: black; }
    .timeline-dot.current { background: #fd8a09; color: black; }
    .timeline-dot.future { background: #374151; color: white; }
    .timeline-dot:hover { transform: scale(1.4) !important; }
    .timeline-dot.completed:hover { box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.3) !important; }
    .timeline-dot.current:hover { box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.3) !important; }
    .timeline-dot.future:hover { box-shadow: 0 0 0 4px rgba(55, 65, 81, 0.3) !important; }
    body.light-mode .timeline-dot { color: black !important; }
  
    .timeline-line { 
      width: 2px; 
      height: 25px; 
      background: #374151; 
      transition: all 0.3s ease; 
      flex-shrink: 0; 
    }
    .timeline-line.completed { background: #4ade80; }

    #timeline-tooltip {
      position: fixed; 
      background: rgba(0,0,0,0.9); 
      color: white; 
      padding: 8px 12px; 
      border-radius: 8px;
      font-size: 12px; 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
      pointer-events: none;
      z-index: 1001; 
      opacity: 0; 
      transition: all 0.2s ease; 
      white-space: nowrap;
    }
    .tooltip-text { opacity: 0.9; font-size: 11px; font-weight: 600; }
  
    #timeline-full-list {
      position: fixed; 
      background: rgba(20,20,20,0.95); 
      color: white; 
      padding: 12px 16px; 
      border-radius: 12px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
      backdrop-filter: blur(20px);
      z-index: 1002; 
      opacity: 0; 
      pointer-events: none; 
      transition: opacity 0.3s ease;
      max-height: 80vh; 
      overflow-y: auto; 
      border: 1px solid rgba(255,255,255,0.1);
    }
    #timeline-full-list ul { list-style: none; padding: 0; margin: 0; font-size: 11px; }
    #timeline-full-list li { padding: 4px 0; opacity: 0.8; white-space: nowrap; }
  
    body.light-mode #timeline-nav { 
      background: rgba(255,255,255,0.95) !important; 
      border-color: rgba(0,0,0,0.1) !important; 
      box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important; 
    }
    body.light-mode .timeline-dot.future { background: #d1d5db; }
    body.light-mode .timeline-line { background: #d1d5db; }
    body.light-mode #timeline-tooltip { 
      background: rgba(255,255,255,0.95); 
      color: #333; 
      border: 1px solid rgba(0,0,0,0.1); 
    }
    body.light-mode #timeline-full-list { 
      background: rgba(255,255,255,0.95); 
      color: #333; 
      border: 1px solid rgba(0,0,0,0.1); 
    }
  
    /* ======= GENERAL DARK/LIGHT STYLES ======= */
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
    html { scroll-behavior: smooth; } 
    h1, h2, h3, h4, h5, h6 { scroll-margin-top: 20px; }
    a:link, a:visited { color: #4aa3ff !important; } 
    a:hover, a:active { color: #82c7ff !important; }
    blockquote { 
      border-left: 4px solid #569cd6; 
      padding-left: 12px; 
      margin-left: 0; 
      font-style: italic; 
      color: #cccccc; 
      background: #2a2a2a; 
      transition: all 0.3s ease; 
    }
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
    body.light-mode a:link, body.light-mode a:visited { color: #0066cc !important; }
    body.light-mode a:hover, body.light-mode a:active { color: #004499 !important; }
    body.light-mode blockquote { 
      border-left: 4px solid #0066cc; 
      color: #555; 
      background: #f5f5f5; 
    }
    body.light-mode table { background: #ffffff; color: #333333; }
    body.light-mode table, body.light-mode th, body.light-mode td { border: 1px solid #ddd; }
    body.light-mode th { background: #f5f5f5; }
    body.light-mode tr:nth-child(even) { background: #f9f9f9; }
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
    body.light-mode pre, body.light-mode code { 
      background-color: #f8f8f8 !important; 
      color: #333333 !important; 
    }
    .copy-btn { 
      position: absolute; 
      top: 3px; 
      right: 8px; 
      background: #2d2d2d; 
      color: #d4d4d4; 
      border: 1px solid #444; 
      border-radius: 6px; 
      font-size: 12px; 
      padding: 2px 6px; 
      cursor: pointer; 
      opacity: 0.6; 
      z-index: 5; 
      transition: all 0.3s ease; 
    }
    .copy-btn:hover { opacity: 1; background: #3a3a3a; }
    body.light-mode .copy-btn { background: #e0e0e0; color: #333; border-color: #ccc; }
    body.light-mode .copy-btn:hover { background: #d0d0d0; }
    .k, .kp, .kt, .kc, .kd, .kn { color: #c586c0 !important; } 
    .nf, .nc, .nn { color: #4fc1ff !important; } 
    .n { color: #ffffff !important; } 
    .s, .sb, .sc, .sd, .s1, .s2, .sa, .se { color: #6a9955 !important; } 
    .m, .mf, .mi, .il { color: #d19a66 !important; } 
    .c, .cm, .cpf { color: #6a9955 !important; font-style: italic !important; } 
    .o, .p { color: #d4d4d4 !important; }
    body.light-mode .k, body.light-mode .kp, body.light-mode .kt, body.light-mode .kc, body.light-mode .kd, body.light-mode .kn { color: #8B008B !important; } 
    body.light-mode .nf, body.light-mode .nc, body.light-mode .nn { color: #0000FF !important; } 
    body.light-mode .n { color: #000000 !important; } 
    body.light-mode .s, body.light-mode .sb, body.light-mode .sc, body.light-mode .sd, body.light-mode .s1, body.light-mode .s2, body.light-mode .sa, body.light-mode .se { color: #008000 !important; } 
    body.light-mode .m, body.light-mode .mf, body.light-mode .mi, body.light-mode .il { color: #d19a66 !important; } 
    body.light-mode .c, body.light-mode .cm, body.light-mode .cpf { color: #008000 !important; font-style: italic !important; } 
    body.light-mode .o, body.light-mode .p { color: #333333 !important; }
    
    /* ======= MOBILE RESPONSIVE ======= */
    @media (max-width: 768px) { 
      :root { --button-size: 36px; }
      body { margin-right: 60px !important; }
      .jp-Notebook { max-width: calc(100% - 60px) !important; }
      .jp-Cell { margin-right: 10px !important; }
      .button-container { top: 10px; right: 10px; padding: 6px; gap: 2px; }
      .code-toggle-btn svg,
      .theme-toggle-btn svg,
      .report-issue-btn svg,
      .download-btn svg {
        width: 18px !important;
        height: 18px !important;
      }
      #timeline-nav { right: 10px !important; padding: 15px 8px !important; gap: 6px !important; } 
      .timeline-line { height: 15px !important; }
    }
    
    @media (max-width: 480px) { 
      :root { --button-size: 32px; }
      body { margin-right: 50px !important; }
      .jp-Notebook { max-width: calc(100% - 50px) !important; }
      .jp-Cell { margin-right: 5px !important; }
      .button-container { padding: 4px; gap: 2px; top: 10px; right: 10px; }
      .code-toggle-btn svg,
      .theme-toggle-btn svg,
      .report-issue-btn svg,
      .download-btn svg {
        width: 16px !important;
        height: 16px !important;
      }
      #timeline-nav { right: 5px !important; padding: 10px 6px !important; gap: 4px !important; transform: translateY(-50%) scale(0.9) !important; border-radius: 20px !important; } 
      .timeline-dot { width: 16px !important; height: 16px !important; font-size: 10px !important; margin: -6px !important; }
      .timeline-line { height: 12px !important; width: 1px !important; }
      #timeline-tooltip { font-size: 10px !important; padding: 6px 8px !important; }
      #timeline-full-list { font-size: 10px !important; padding: 8px 10px !important; max-height: 60vh !important; }
    }
    
    @media (max-width: 360px) {
      :root { --button-size: 28px; }
      body { margin-right: 40px !important; }
      .jp-Notebook { max-width: calc(100% - 40px) !important; }
      .button-container { gap: 1px; padding: 3px; }
      .code-toggle-btn svg,
      .theme-toggle-btn svg,
      .report-issue-btn svg,
      .download-btn svg {
        width: 14px !important;
        height: 14px !important;
      }
      #timeline-nav { transform: translateY(-50%) scale(0.8) !important; padding: 8px 4px !important; gap: 3px !important; }
      .timeline-dot { width: 14px !important; height: 14px !important; font-size: 9px !important; }
      .timeline-line { height: 10px !important; }
    }
    </style>
    """
  
    toggle_js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
      
      // SVG Icon Functions
      function createCodeIcon() {
        return `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="6,7 2,12 6,17"></polyline>
          <line x1="13" y1="5" x2="11" y2="19"></line>
          <polyline points="18,7 22,12 18,17"></polyline>
        </svg>`;
      }

      function createCodeHiddenIcon() {
        return `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="8,6 2,12 8,18"></polyline>
          <polyline points="16,6 22,12 16,18"></polyline>
        </svg>`;
      }

      function createSunIcon() {
        return `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>`;
      }

      function createMoonIcon() {
        return `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>`;
      }

      function createQuestionIcon() {
        return `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="9"></circle>
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
          <circle cx="12" cy="17" r="0.5" fill="currentColor"></circle>
        </svg>`;
      }

      function createDownloadIcon() {
        return `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
          <polyline points="7,10 12,15 17,10"></polyline>
          <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>`;
      }

      // Create button container
      var buttonContainer = document.createElement("div");
      buttonContainer.className = "button-container";

      // Code toggle button (first button)
      var codeToggleBtn = document.createElement("button");
      codeToggleBtn.className = "code-toggle-btn";
      codeToggleBtn.innerHTML = createCodeIcon();
      codeToggleBtn.title = "Hide code cells";
      
      var codeVisible = true;
      
      // Code toggle functionality
      function toggleCodeVisibility() {
        codeVisible = !codeVisible;
        
        if (codeVisible) {
          // Show code - use wider content to match hidden state
          document.body.classList.remove('code-hidden');
          codeToggleBtn.classList.remove('code-hidden');
          codeToggleBtn.innerHTML = createCodeIcon();
          codeToggleBtn.title = "Hide code cells";
        } else {
          // Hide code - use same width as visible state
          document.body.classList.add('code-hidden');
          codeToggleBtn.classList.add('code-hidden');
          codeToggleBtn.innerHTML = createCodeHiddenIcon();
          codeToggleBtn.title = "Show code cells";
        }
        
        // Save preference
        localStorage.setItem('code-visibility', codeVisible ? 'visible' : 'hidden');
      }
      
      codeToggleBtn.addEventListener("click", toggleCodeVisibility);
      
      // Initialize code visibility from localStorage
      var savedCodeVisibility = localStorage.getItem('code-visibility') || 'visible';
      if (savedCodeVisibility === 'hidden') {
        codeVisible = true; // Will be toggled to false
        toggleCodeVisibility();
      }

      // Theme toggle button
      var themeToggleBtn = document.createElement("button");
      themeToggleBtn.className = "theme-toggle-btn";
      themeToggleBtn.title = "Toggle theme";
      
      // Create theme icons - only dark and light modes
      var darkIcon = document.createElement("span");
      darkIcon.className = "theme-icon dark";
      darkIcon.innerHTML = createMoonIcon();
      
      var lightIcon = document.createElement("span");
      lightIcon.className = "theme-icon light";
      lightIcon.innerHTML = createSunIcon();
      
      themeToggleBtn.appendChild(darkIcon);
      themeToggleBtn.appendChild(lightIcon);
      
      // Theme management - only dark and light
      var currentTheme = 'dark'; // Will be set based on system preference
      var themeIcons = {
        dark: darkIcon,
        light: lightIcon
      };
      
      // Check for system preference
      function getSystemTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      
      // Apply theme to DOM
      function applyTheme(theme) {
        // Remove all theme classes
        document.body.classList.remove('light-mode', 'dark-mode');
        
        // Apply the theme class
        if (theme === 'light') {
          document.body.classList.add('light-mode');
        } else {
          document.body.classList.add('dark-mode');
        }
      }
      
      // Update theme toggle UI
      function updateThemeToggle() {
        // Remove active class from all icons
        Object.keys(themeIcons).forEach(function(key) {
          themeIcons[key].classList.remove('active');
        });
        
        // Add active class to current theme icon
        themeIcons[currentTheme].classList.add('active');
        
        // Update tooltip
        var themeNames = {
          dark: 'Theme: Dark',
          light: 'Theme: Light'
        };
        themeToggleBtn.title = themeNames[currentTheme];
      }
      
      // Theme toggle click handler - only toggle between dark and light
      function toggleTheme() {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        applyTheme(currentTheme);
        updateThemeToggle();
        
        // Save preference
        localStorage.setItem('theme-preference', currentTheme);
      }
      
      themeToggleBtn.addEventListener("click", toggleTheme);
      
      // Initialize theme - always start with system preference on page load
      currentTheme = getSystemTheme();
      applyTheme(currentTheme);
      updateThemeToggle();
      
      // Real-time system theme change detection - updates without page reload
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        // Automatically detect and apply system theme changes
        currentTheme = getSystemTheme();
        applyTheme(currentTheme);
        updateThemeToggle();
        
        // Optional: Clear any saved manual preference since we're following system
        localStorage.removeItem('theme-preference');
        
        console.log('System theme changed to:', currentTheme); // For debugging
      });

      // Extract notebook name
      function getNotebookName() {
        var url = window.location.href;
        var filename = url.split('/').pop();
      
        if (filename.includes('.html')) {
          // Remove extension
          var nameWithoutExt = filename.replace('.html', '');
      
          // Take everything after the first '-'
          var parts = nameWithoutExt.split('-');
          var titlePart = parts.slice(1).join('-'); // everything after first "-"
      
          // Replace underscores with spaces, leave everything else as is
          return titlePart.replace(/_/g, ' ');
        }
        return 'Unknown Notebook';
      }

      function getIpynbFilename() {
        var url = window.location.href;
        var filename = url.split('/').pop();
        if (filename.includes('.html')) {
          return filename.replace('.html', '.ipynb');
        }
        return 'notebook.ipynb';
      }

      // Report issue button - question mark icon
      var reportIssueBtn = document.createElement("a");
      reportIssueBtn.className = "report-issue-btn";
      reportIssueBtn.innerHTML = createQuestionIcon();
      reportIssueBtn.title = "Have questions about this notebook?";
      reportIssueBtn.target = "_blank";
      reportIssueBtn.rel = "noopener noreferrer";
      reportIssueBtn.style.color = "inherit";  // Ensure it inherits the right color
      
      var notebookName = getNotebookName();
      var issueTitle = "[Tutorial Content Issue] " + notebookName;
      var issueBody = encodeURIComponent("[" + notebookName + "](" + window.location.href + ")\\n\\nMention your queries below: \\n");
      reportIssueBtn.href = "https://github.com/meluron-codecafe/DevQuest/issues/new?assignees=ankit0anand0&labels=tutorials&projects=&template=&title=" + encodeURIComponent(issueTitle) + "&body=" + issueBody;

      // Download button - down arrow icon
      var downloadBtn = document.createElement("a");
      downloadBtn.className = "download-btn";
      downloadBtn.innerHTML = createDownloadIcon();
      downloadBtn.title = "Download .ipynb file";
      downloadBtn.target = "_blank";
      downloadBtn.rel = "noopener noreferrer";
      downloadBtn.style.color = "inherit";  // Ensure it inherits the right color
      
      var ipynbFilename = getIpynbFilename();
      downloadBtn.href = "../notebooks/" + ipynbFilename;
      downloadBtn.download = ipynbFilename;

      
      // Add components to container (Code Toggle → Theme Toggle → Report Issue → Download)
      buttonContainer.appendChild(codeToggleBtn);
      buttonContainer.appendChild(themeToggleBtn);
      buttonContainer.appendChild(reportIssueBtn);
      buttonContainer.appendChild(downloadBtn);
      document.body.appendChild(buttonContainer);

      // Timeline functionality
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
          dot.textContent = index + 1;

          dot.addEventListener("click", (e) => {
            e.preventDefault();
            heading.scrollIntoView({ behavior: "smooth" });
          });

          function cleanHeadingText(heading) {
            let text = heading.textContent.trim();
            text = text.replace(/[\u00B6]/g, ''); 
            return text;
          }

          let hoverTimeout;
          dot.addEventListener("mouseenter", () => {
            var text = cleanHeadingText(heading);
            if (text.length > 40) text = text.substring(0, 40) + "...";
            var rect = dot.getBoundingClientRect();
            tooltip.innerHTML = '<div class="tooltip-text">' + text + '</div>';
            tooltip.style.top = (rect.top + rect.height / 2 - tooltip.offsetHeight / 2) + 'px';
            tooltip.style.left = (rect.left - tooltip.offsetWidth - 10) + 'px';
            tooltip.style.opacity = '1';

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
        for (var i = 0; i < headings.length; i++) { 
          if (headings[i].offsetTop <= scrollPos) currentIndex = i; 
        }

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
      window.addEventListener("scroll", () => { 
        clearTimeout(scrollTimeout); 
        scrollTimeout = setTimeout(updateTimeline, 50); 
      });

      // Copy button functionality for code blocks
      document.querySelectorAll("div.highlight").forEach(block => {
        var btn = document.createElement("button");
        btn.innerHTML = "Copy"; 
        btn.className = "copy-btn"; 
        btn.title = "Copy code";
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

      // Initialize everything
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