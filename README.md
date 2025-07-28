
# Adobe Hackathon - PDF Document Structure Extraction

**Team Name:** WiNNER  
**Institution:** Vivekanand Institute of Professional Studies, GGSIPU  
**Team Members:** Yuvraj Choudhary, Anmol Dua, Meet Goyal

## Project Structure

```
ADOBE-1A/
├── Challenge_1a/
│   ├── input/               # Input PDF files (mounts to /app/input in Docker)
│   ├── output/              # Output JSON files (mounts to /app/output in Docker)
│   ├── main.py              # Main orchestrator script - entry point
│   ├── process_pdfs.py      # PDF processing module with extraction logic
│   ├── Dockerfile           # Docker container configuration
│   ├── requirements.txt     # Python dependencies
│   ├── approach_explanation.md  # Detailed methodology explanation
│   └── README.md            # Project documentation
├── input/                   # Alternative input directory (empty)
├── output/                  # Alternative output directory (empty)
└── README.md                # This file
```

## Solution Overview

Our solution implements a **two-tier architecture** for robust PDF document structure extraction:

### Core Components

1. **Main Orchestrator (`main.py`)**: 
   - Entry point that coordinates the entire workflow
   - Discovers and processes all PDFs in input directory and subdirectories
   - Provides centralized logging and error handling
   - Implements the `ChallengeOrchestrator` class

2. **PDF Processing Engine (`process_pdfs.py`)**: 
   - Contains the `PDFStructureExtractor` class with core extraction logic
   - Handles font analysis, heading detection, and outline generation
   - Can be used standalone or through the orchestrator

### Technical Approach

1. **PDF Text Extraction**: Uses PyMuPDF (fitz) to extract text blocks with font metadata, sizes, and positions from each PDF page.
2. **Intelligent Heading Detection**: Multi-factor scoring system that identifies headings based on:
   - Font size relative to document average
   - Font weight (boldness) and style
   - Text patterns (numbering, capitalization)
   - Positioning and spacing analysis
3. **Hierarchical Outline Generation**: Detected headings are classified into levels (H1, H2, H3) and structured into a document outline.
4. **Batch Processing**: Orchestrator automatically discovers and processes all PDFs in input directory and subdirectories.
5. **Containerized Deployment**: Fully Dockerized workflow with volume mounting for seamless input/output handling.

## How to Run

**Prerequisites:** Docker installed on your system

1. **Navigate to the project directory:**
   ```sh
   cd Challenge_1a
   ```

2. **Build the Docker image:**
   ```sh
   docker build --platform linux/amd64 -t pdf-orchestrator .
   ```

3. **Run the container:**
   ```sh
   # On Windows:
   docker run --rm -v "%cd%\input":/app/input:ro -v "%cd%\output":/app/output pdf-orchestrator
   
   # On Linux/Mac:
   docker run --rm -v "$(pwd)/input":/app/input:ro -v "$(pwd)/output":/app/output pdf-orchestrator
   ```

### Alternative: Direct Python Execution

```sh
# Install dependencies
pip install -r requirements.txt

# Run the orchestrator
python main.py

# Or run the processor directly
python process_pdfs.py
```

## Output

For each input PDF, a corresponding `*_outline.json` file is generated in the `output/` directory with the following structure:

```json
{
    "title": "Document Title",
    "outline": [
        {
            "level": "H1",
            "text": "Main Heading",
            "page": 1
        },
        {
            "level": "H2", 
            "text": "Sub Heading",
            "page": 1
        }
    ],
    "extraction_timestamp": "2025-07-28T09:03:31.721440",
    "total_headings": 9
}
```

## Key Features

- **Flexible Input Structure**: Processes PDFs from any folder structure within input directory
- **Comprehensive Logging**: Detailed extraction logs for debugging and monitoring
- **Docker Integration**: Consistent execution environment across different systems
- **Timestamp Tracking**: Each output includes extraction timestamp for audit trails
- **Error Handling**: Robust error handling with detailed logging for troubleshooting

## Dependencies

- **Python 3.9+**
- **PyMuPDF (fitz)**: PDF text extraction and analysis
- **PyPDF2**: Additional PDF processing capabilities
- **Docker**: For containerized execution

See `Challenge_1a/requirements.txt` for complete dependency list.

## Project Files

- **`main.py`**: Orchestrator entry point with `ChallengeOrchestrator` class
- **`process_pdfs.py`**: Core extraction logic with `PDFStructureExtractor` class  
- **`approach_explanation.md`**: Detailed technical methodology and Docker setup instructions
- **`Dockerfile`**: Container configuration optimized for PDF processing
