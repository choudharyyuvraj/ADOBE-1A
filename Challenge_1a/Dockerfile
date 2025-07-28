FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts
COPY main.py ./
COPY process_pdfs.py ./

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set up logging
ENV PYTHONUNBUFFERED=1

# Run the main orchestrator
CMD ["python", "main.py"]
