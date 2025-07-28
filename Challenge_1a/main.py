#!/usr/bin/env python3
"""
Adobe Hackathon 2025: "Connecting the Dots" - Final Orchestrator
"""
import json, logging
from pathlib import Path
from process_pdfs import PDFStructureExtractor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChallengeOrchestrator:
    def __init__(self, input_dir="input", output_dir="output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.structure_extractor = PDFStructureExtractor()
        

    def run_round_1a(self, folder_path: Path):
        logger.info(f"--- Running Round 1A on folder: {folder_path.name} ---")
        pdf_files = list(folder_path.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files: {[f.name for f in pdf_files]}")
        
        if not pdf_files: 
            logger.warning(f"No PDF files found in {folder_path}")
            return

        output_1a_dir = self.output_dir / folder_path.name
        output_1a_dir.mkdir(exist_ok=True)
        logger.info(f"Output directory: {output_1a_dir}")
        
        for pdf_file in pdf_files:
            try:
                result = self.structure_extractor.extract_pdf_outline(str(pdf_file))
                output_path = output_1a_dir / f"{pdf_file.stem}_outline.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                logger.info(f"Saved 1A outline to {output_path}")
            except Exception as e:
                logger.error(f"Error in Round 1A on {pdf_file.name}: {e}")

    

    def run(self):
        logger.info("Starting Adobe Hackathon Submission Orchestrator")
        logger.info(f"Input directory: {self.input_dir.resolve()}")
        logger.info(f"Output directory: {self.output_dir.resolve()}")
        
        if not self.input_dir.exists():
            logger.error(f"Input directory does not exist: {self.input_dir}")
            return
        
        # Process PDFs directly in input folder
        direct_pdfs = list(self.input_dir.glob("*.pdf"))
        if direct_pdfs:
            logger.info(f"Found {len(direct_pdfs)} PDFs directly in input folder")
            self.process_pdfs_in_folder(self.input_dir, "input")
        
        # Process PDFs in all subfolders
        subfolders = [f for f in self.input_dir.iterdir() if f.is_dir()]
        logger.info(f"Found subfolders: {[f.name for f in subfolders]}")
        
        for folder in subfolders:
            pdf_files = list(folder.glob("*.pdf"))
            if pdf_files:
                logger.info(f"Processing {len(pdf_files)} PDFs in folder: {folder.name}")
                self.process_pdfs_in_folder(folder, folder.name)
            else:
                logger.info(f"No PDFs found in folder: {folder.name}")
        
        logger.info("All tasks completed.")

    def process_pdfs_in_folder(self, folder_path: Path, folder_name: str):
        """Process all PDFs in a given folder."""
        logger.info(f"--- Processing PDFs in folder: {folder_name} ---")
        pdf_files = list(folder_path.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files: {[f.name for f in pdf_files]}")
        
        if not pdf_files: 
            logger.warning(f"No PDF files found in {folder_path}")
            return

        output_dir = self.output_dir / folder_name
        output_dir.mkdir(exist_ok=True)
        logger.info(f"Output directory: {output_dir}")
        
        for pdf_file in pdf_files:
            try:
                result = self.structure_extractor.extract_pdf_outline(str(pdf_file))
                output_path = output_dir / f"{pdf_file.stem}_outline.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                logger.info(f"Saved outline to {output_path}")
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {e}")

if __name__ == "__main__":
    ChallengeOrchestrator().run()