#!/usr/bin/env python3
"""
IPCC Chapter Processing Pipeline
A declarative pipeline for downloading, cleaning, and enriching IPCC chapters.

Usage:
    python ipcc_pipeline.py --config pipeline_config.yaml --source wg1_chapter02
    python ipcc_pipeline.py --config pipeline_config.yaml --all
"""

import argparse
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import json

# Pipeline components - using absolute imports
from pipeline.downloader import WebDownloader
from pipeline.cleaner import ContentCleaner
from pipeline.structurer import ContentStructurer
from pipeline.chunker import ContentChunker
from pipeline.dictionary import DictionaryExtractor
from pipeline.encyclopedia import EncyclopediaBuilder
from pipeline.quality import QualityChecker


@dataclass
class PipelineConfig:
    """Configuration for the IPCC processing pipeline."""
    config_file: Path
    source_name: str = None
    process_all: bool = False
    output_dir: Path = Path("output")
    log_level: str = "INFO"


class IPCCPipeline:
    """
    Main pipeline orchestrator for processing IPCC chapters.
    
    This pipeline follows a declarative configuration approach where each stage
    is defined in YAML and can be enabled/disabled independently.
    """
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.pipeline_config = self._load_config()
        self.setup_logging()
        
        # Initialize pipeline components
        self.downloader = WebDownloader(self.pipeline_config['stages']['download'])
        self.cleaner = ContentCleaner(self.pipeline_config['stages']['clean'])
        self.structurer = ContentStructurer(self.pipeline_config['stages']['structure'])
        self.chunker = ContentChunker(self.pipeline_config['stages']['chunk'])
        self.dictionary_extractor = DictionaryExtractor(self.pipeline_config['stages']['dictionary'])
        self.encyclopedia_builder = EncyclopediaBuilder(self.pipeline_config['stages']['encyclopedia'])
        self.quality_checker = QualityChecker(self.pipeline_config['quality_checks'])
        
    def _load_config(self) -> Dict[str, Any]:
        """Load the pipeline configuration from YAML."""
        with open(self.config.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.output_dir / 'pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        """Run the complete pipeline."""
        self.logger.info(f"Starting IPCC pipeline: {self.pipeline_config['pipeline']['name']}")
        
        sources = self._get_sources()
        
        for source in sources:
            try:
                self.logger.info(f"Processing source: {source['name']}")
                self._process_source(source)
            except Exception as e:
                self.logger.error(f"Error processing {source['name']}: {e}")
                if not self.pipeline_config['error_handling']['continue_on_error']:
                    raise
    
    def _get_sources(self) -> List[Dict[str, Any]]:
        """Get the list of sources to process."""
        if self.config.process_all:
            return self.pipeline_config['sources']
        elif self.config.source_name:
            return [s for s in self.pipeline_config['sources'] 
                   if s['name'] == self.config.source_name]
        else:
            raise ValueError("Must specify either --source or --all")
    
    def _process_source(self, source: Dict[str, Any]):
        """Process a single source through all pipeline stages."""
        source_dir = self.config.output_dir / source['working_group'] / source['chapter']
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Stage 1: Download
        if self.pipeline_config['stages']['download']['enabled']:
            self.logger.info(f"Downloading {source['name']} from {source['url']}")
            html_content = self.downloader.download(source['url'])
            download_path = source_dir / "raw.html"
            download_path.write_text(html_content, encoding='utf-8')
        
        # Stage 2: Clean
        if self.pipeline_config['stages']['clean']['enabled']:
            self.logger.info(f"Cleaning content for {source['name']}")
            cleaned_content = self.cleaner.clean(html_content)
            cleaned_path = source_dir / "cleaned.html"
            cleaned_path.write_text(cleaned_content, encoding='utf-8')
        
        # Stage 3: Structure (add paragraph IDs)
        if self.pipeline_config['stages']['structure']['enabled']:
            self.logger.info(f"Adding structure and IDs to {source['name']}")
            structured_content = self.structurer.structure(cleaned_content)
            structured_path = source_dir / "structured.html"
            structured_path.write_text(structured_content, encoding='utf-8')
        
        # Stage 4: Chunk
        if self.pipeline_config['stages']['chunk']['enabled']:
            self.logger.info(f"Chunking content for {source['name']}")
            chunks = self.chunker.chunk(structured_content)
            chunks_path = source_dir / "chunks.json"
            chunks_path.write_text(json.dumps(chunks, indent=2), encoding='utf-8')
        
        # Stage 5: Dictionary
        if self.pipeline_config['stages']['dictionary']['enabled']:
            self.logger.info(f"Extracting dictionary for {source['name']}")
            dictionary = self.dictionary_extractor.extract(structured_content)
            dict_path = source_dir / "dictionary.json"
            dict_path.write_text(json.dumps(dictionary, indent=2), encoding='utf-8')
        
        # Stage 6: Encyclopedia
        if self.pipeline_config['stages']['encyclopedia']['enabled']:
            self.logger.info(f"Building encyclopedia for {source['name']}")
            encyclopedia = self.encyclopedia_builder.build(dictionary)
            enc_path = source_dir / "encyclopedia.json"
            enc_path.write_text(json.dumps(encyclopedia, indent=2), encoding='utf-8')
        
        # Quality checks
        self.logger.info(f"Running quality checks for {source['name']}")
        quality_report = self.quality_checker.check(structured_content, source)
        quality_path = source_dir / "quality_report.json"
        quality_path.write_text(json.dumps(quality_report, indent=2), encoding='utf-8')
        
        self.logger.info(f"Completed processing {source['name']}")


def main():
    """Main entry point for the pipeline."""
    parser = argparse.ArgumentParser(description="IPCC Chapter Processing Pipeline")
    parser.add_argument("--config", type=Path, required=True, 
                       help="Path to pipeline configuration YAML file")
    parser.add_argument("--source", type=str, 
                       help="Name of specific source to process")
    parser.add_argument("--all", action="store_true", 
                       help="Process all sources in configuration")
    parser.add_argument("--output-dir", type=Path, default=Path("output"),
                       help="Output directory for processed files")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    if not args.source and not args.all:
        parser.error("Must specify either --source or --all")
    
    config = PipelineConfig(
        config_file=args.config,
        source_name=args.source,
        process_all=args.all,
        output_dir=args.output_dir,
        log_level=args.log_level
    )
    
    pipeline = IPCCPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main() 