#!/usr/bin/env python3

#!/usr/bin/env python3

from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
import nbformat
from pathlib import Path
import argparse
import os

root_dir = Path(__file__).parent.resolve()

def convert_to_html(notebook_path: Path) -> str:
	notebook = nbformat.read(notebook_path, as_version=4)
	exporter = HTMLExporter()
	body, _ = exporter.from_notebook_node(notebook)
	return body

def strip_hidden_code_cells_from_html(html_content: str) -> (str, int):
	soup = BeautifulSoup(html_content, "html.parser")
	removed = 0
	for input_block in soup.select('.jp-InputArea'):
		pre = input_block.find('pre')
		if pre and pre.text.strip().startswith('#hide'):
			# print(f"Removing input block:\n{pre.text.strip().splitlines()[0]}")
			input_block.decompose()
			removed += 1
	return str(soup), removed

def export_clean_html(ipynb_path: Path):
	html_output_dir = root_dir / "htmls"
	html_output_dir.mkdir(parents=True, exist_ok=True)
	output_path = html_output_dir / f"{ipynb_path.stem}.html"
	
	print(f"{ipynb_path.name}", end=" -> ")
	html = convert_to_html(ipynb_path)
	cleaned_html, removed = strip_hidden_code_cells_from_html(html)
	
	with open(output_path, "w", encoding="utf-8") as f:
		f.write(cleaned_html)
		
	print(f"{output_path.name}\tStatus: ✅\t#hide: {removed}")
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convert .ipynb to HTML and strip #hide code inputs")
	parser.add_argument("-i", "--input", type=str, required=False, help="Path to .ipynb file")
	parser.add_argument("--all", action="store_true", help="Convert all notebooks to HTMLs")
	args = parser.parse_args()
	
	if args.all:
		for notebook in (root_dir / "notebooks").glob("*.ipynb"):
			export_clean_html(notebook)
	else:
		if not args.input:
			parser.error("argument -i/--input is required unless --all is specified")
		export_clean_html(Path(args.input))
	
	