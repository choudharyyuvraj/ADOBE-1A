
import fitz
import json
import statistics
from collections import Counter
import re
import os
import glob

def extract_text_blocks(doc, page_limit=None):
    
    data = []
    total_pages = len(doc) if page_limit is None else min(len(doc), page_limit)
    for idx in range(total_pages):
        page = doc[idx]
        for block in page.get_text("dict", flags=11)["blocks"]:
            for line in block["lines"]:
                for span in line["spans"]:
                    txt = span["text"].strip()
                    if txt:
                        data.append({
                            "text": txt,
                            "font_size": span["size"],
                            "font_name": span["font"],
                            "page": idx + 1,
                            "y_pos": span["bbox"][1]
                        })
    return data

def get_body_text_style(blocks):
    
    if not blocks:
        return 12, "default"
    sizes = [b['font_size'] for b in blocks if b['font_size'] < 20]
    if not sizes:
        sizes = [b['font_size'] for b in blocks]
    try:
        main_size = statistics.mode(sizes)
    except statistics.StatisticsError:
        main_size = max(set(sizes), key=sizes.count)
    return main_size, ""

def identify_and_classify_headings(blocks, body_size):
    
    headings = []
    title = None
    first_page = [b for b in blocks if b['page'] == 1]
    if first_page:
        largest = max(b['font_size'] for b in first_page)
        for b in first_page:
            if b['font_size'] == largest:
                title = {'text': b['text'], 'page': 1}
                break
    candidates = []
    pattern = re.compile(r'^\s*(\d+(\.\d+)*\.?|[A-Z]\.)\s+')
    for b in blocks:
        t = b['text']
        s = b['font_size']
        n = b['font_name'].lower()
        if title and t == title['text'] and b['page'] == 1:
            continue
        score = 0
        if s > body_size + 1:
            score += 2
        if 'bold' in n:
            score += 1
        if pattern.match(t):
            score += 5
        if len(t.split()) < 15:
            score += 1
        if t.isupper() and len(t) > 2:
            score += 1
        if score >= 4:
            candidates.append(b)
    if not candidates:
        return [], title
    styles = sorted(set(b['font_size'] for b in candidates), reverse=True)
    style_map = {style: f"H{i+1}" for i, style in enumerate(styles[:3])}
    for b in candidates:
        if b['font_size'] in style_map:
            headings.append({
                "level": style_map[b['font_size']],
                "text": b['text'],
                "page": b['page'],
                "y_pos": b['y_pos']
            })
    return sorted(headings, key=lambda x: (x['page'], x['y_pos'])), title

def group_text_into_sections(blocks, headings):
    
    sections = []
    if not headings:
        return []
    for i, heading in enumerate(headings):
        start_page = heading['page']
        start_y = heading['y_pos']
        end_page = headings[i+1]['page'] if i + 1 < len(headings) else float('inf')
        end_y = headings[i+1]['y_pos'] if i + 1 < len(headings) else float('inf')
        content = ""
        for block in blocks:
            after = block['page'] > start_page or (block['page'] == start_page and block['y_pos'] > start_y)
            before = block['page'] < end_page or (block['page'] == end_page and block['y_pos'] < end_y)
            is_head = any(h['text'] == block['text'] and h['page'] == block['page'] for h in headings)
            if after and before and not is_head:
                content += block['text'] + "\n"
        sections.append({
            'heading_text': heading['text'],
            'heading_level': heading['level'],
            'page': heading['page'],
            'content': content.strip()
        })
    return sections

def generate_outline_from_pdf(pdf_path):
    
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return json.dumps({"error": f"Could not open PDF: {e}"})
    blocks = extract_text_blocks(doc)
    doc.close()
    if not blocks:
        return json.dumps({"title": "", "outline": []})
    body_size, _ = get_body_text_style(blocks)
    headings, title_info = identify_and_classify_headings(blocks, body_size)
    title = title_info['text'] if title_info else "Untitled"
    outline = [{"level": h['level'], "text": h['text'], "page": h['page']} for h in headings]
    return json.dumps({"title": title, "outline": outline}, indent=4)

def process_pdf_outlines_round_1a(input_base_dir, output_base_dir):
    
    input_dir = os.path.join(input_base_dir, "input")
    print(f"Looking for PDFs in: {input_dir}")
    if not os.path.exists(input_dir):
        print("Input directory does not exist.")
        return
    pdfs = glob.glob(os.path.join(input_dir, "*.pdf"))
    print(f"Found {len(pdfs)} PDF(s): {pdfs}")
    if not pdfs:
        print("No PDF files found.")
        return
    for pdf_path in pdfs:
        try:
            print(f"Processing: {pdf_path}")
            outline = generate_outline_from_pdf(pdf_path)
            base = os.path.splitext(os.path.basename(pdf_path))[0]
            out_file = f"{base}_outline.json"
            out_path = os.path.join(output_base_dir, out_file)
            print(f"Writing output to: {out_path}")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(outline)
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

def main():
    base_dir = "/app"
    out_dir = "/app/output"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "input"), exist_ok=True)
    process_pdf_outlines_round_1a(base_dir, out_dir)

if __name__ == "__main__":
    main()
