
FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /app

# Copy requirements first for better cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy sample dataset structure
COPY sample_dataset/ ./sample_dataset/
COPY process_pdfs.py ./

CMD ["python", "process_pdfs.py"]
