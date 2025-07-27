
# Challenge_1a

**Team Name:** WiNNER  
**Institution:** Vivekanand Institute of Professional Studies, GGSIPU  
**Team Members:** Yuvraj Choudhary, Anmol Dua, Meet Goyal

## Project Structure

```
Challenge_1a/
├── sample_dataset/
│   ├── pdfs/            # Input PDF files (mounts to /app/input in Docker)
│   ├── outputs/         # Output JSON files (mounts to /app/output in Docker)
│   └── schema/          # Output schema definition (if needed)
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Main processing script
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
   docker build --platform linux/amd64 -t pdf-processor .
   ```
2. **Run the container:**
   ```sh
   docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdf-processor
   ```
   (On Windows, use `%cd%` instead of `$(pwd)`)

## Output

For each input PDF, a corresponding `*_outline.json` file is generated in `sample_dataset/outputs/`.

## Dependencies

- Python 3.9+
- PyMuPDF

See `requirements.txt` for details.
