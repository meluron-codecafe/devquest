#!/usr/bin/env python3

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
	- Add 'keywords' class to the first <p> in the first markdown cell.
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
	keywords_text = ""
	first_markdown = soup.select_one('.jp-RenderedHTMLCommon p')
	if first_markdown:
		first_markdown['class'] = first_markdown.get('class', []) + ['keywords']
		keywords_text = first_markdown.get_text(strip=True)
		
	return str(soup), removed, keywords_text

def export_clean_html(ipynb_path: Path):
	html_output_dir = root_dir / "htmls"
	html_output_dir.mkdir(parents=True, exist_ok=True)
	output_path = html_output_dir / f"{ipynb_path.stem}.html"
	
	html = convert_to_html(ipynb_path)
	cleaned_html, removed, keywords = strip_hidden_code_cells_and_tag_keywords(html)
	
	with open(output_path, "w", encoding="utf-8") as f:
		f.write(cleaned_html)
		
	print(f"{output_path.name}\n\tStatus: ✅\t#hide: {removed}\tKeywords: {keywords}")
	return keywords

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
	
	category = match.group("category").upper()
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
			keywords = export_clean_html(notebook)
			category, topic, number = extract_info_from_filename(notebook)
			if category:
				csv_rows.append([
					category,
					topic,
					keywords,
					number.zfill(2),
					notebook.name,
					f"{notebook.stem}.html",
				])
		
		# Save CSV with correct header
		csv_file = root_dir / "tutorials.csv"
		with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
			writer = csv.writer(f)
			writer.writerow(["category", "topic", "keywords", "number", "notebook", "html"])
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
			header, rows = ["category", "topic", "subtopics", "number", "notebook", "html", "keywords"], []
			
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
		rows.sort(key=lambda x: (x[0], int(x[3])))
		
		# Save back to CSV
		with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
			writer = csv.writer(f)
			writer.writerow(header)
			writer.writerows(rows)
			
		print(f"✅ {'Updated' if updated else 'Added'} row for {notebook_path.name} in {csv_file}")
		
		