
# Challenge_1a

## Project Structure

```
Challenge_1a/
├── input/               # Input PDF files (mounts to /app/input in Docker)
├── output/              # Output JSON files (mounts to /app/output in Docker)
├── Dockerfile           # Docker container configuration
├── main.py              # Main orchestrator script
├── process_pdfs.py      # PDF processing module
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Approach

1. **PDF Extraction**: The script uses PyMuPDF to extract text blocks, font sizes, and positions from each PDF page.
2. **Heading Detection**: A scoring system identifies headings based on font size, boldness, numbering, and capitalization.
3. **Outline Generation**: Detected headings are classified (H1, H2, H3) and used to build a structured outline for each document.
4. **Batch Processing**: All PDFs in the input directory are processed, and their outlines are saved as JSON files in the output directory.
5. **Dockerized Workflow**: The project is containerized for reproducibility. Input/output folders are mounted at runtime for easy data exchange.

## How to Run

1. **Build the Docker image:**
   ```sh
   docker build --platform linux/amd64 -t pdf-orchestrator .
   ```
2. **Run the container:**
   ```sh
   # On Windows (from Challenge_1a directory):
   docker run --rm -v "%cd%\input":/app/input:ro -v "%cd%\output":/app/output pdf-orchestrator
   
   # On Linux/Mac (from Challenge_1a directory):
   docker run --rm -v "$(pwd)/input":/app/input:ro -v "$(pwd)/output":/app/output pdf-orchestrator
   ```

## Output

For each input PDF, a corresponding `*_outline.json` file is generated in the `output/` directory.

## Dependencies

- Python 3.9+
- PyMuPDF

See `requirements.txt` for details.
