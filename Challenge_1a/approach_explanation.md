# Approach Explanation: PDF Outline Extraction Project

## Overview
This project automates the extraction of structured outlines from PDF documents using Python and the PyMuPDF library (`fitz`). It processes batches of PDFs, identifies the hierarchical structure (titles, headings, subheadings), and exports that structure as JSON outlines. To ensure portability and consistency, the entire workflow is containerized with Docker.

## Methodology

1. **Text Block Extraction**  
   Each PDF is opened with PyMuPDF. For every page, the script extracts text spans along with metadata:  
   - **Text content**  
   - **Font size**  
   - **Font name**  
   - **Page number**  
   - **Vertical position**  
   This granular data distinguishes regular body text from potential headings.

2. **Body Text Style Identification**  
   To establish a baseline, the script filters out unusually large font sizes (likely headings) and computes the statistical mode of the remaining sizes. This “body text size” is used to flag larger text spans as candidate headings.

3. **Heading Detection Scoring**  
   Each text span is scored against five criteria:  
   - Font size > body baseline (+2)  
   - Bold font (+1)  
   - Regex match of numbering patterns (e.g., “1.”, “1.1.”, “A.”) (+5)  
   - Short length (<15 words) (+1)  
   - All-caps text longer than 2 characters (+1)  
   Spans scoring ≥4 points become heading candidates.

4. **Heading Level Classification**  
   Candidates are grouped by font size and sorted descending. The top three sizes map to `H1`, `H2`, and `H3`, reflecting document hierarchy levels.

5. **Outline Construction**  
   Detected headings are ordered by page and vertical position. The script builds a JSON array where each entry contains:  
   ```json
   {
     "level": "H1",
     "text": "Section Title",
     "page": 3
   }

6. **Batch Processing & Output
    The script scans /app/input (mounted from sample_dataset/pdfs) for .pdf files.
    For each PDF, it writes the JSON outline to /app/output (mounted from sample_dataset/outputs).
    Debug logs print progress and any errors.
    Containerization with Docker
    Dockerfile

Containerization with Docker
Dockerfile

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY sample_dataset/ ./sample_dataset/
COPY [process_pdfs.py](http://_vscodecontentref_/0) ./
CMD ["python", "process_pdfs.py"]
```

Build & Run

# Build the image
docker build --platform linux/amd64 -t pdf-processor .

# Run the container (Linux/macOS)
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  pdf-processor

# On Windows PowerShell, replace $(pwd) with ${PWD}:
docker run --rm \
  -v ${PWD}\\sample_dataset\\pdfs:/app/input:ro \
  -v ${PWD}\\sample_dataset\\outputs:/app/output \
  --network none \
  pdf-processor


After running, check sample_dataset/outputs for the generated outline files. Ensure your input PDFs are valid and non-empty before executing.After running, check sample_dataset/outputs for the generated outline files. Ensure your input PDFs are valid and non-empty before executing.