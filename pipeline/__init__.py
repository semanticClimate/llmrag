"""
IPCC Pipeline Components

This package contains the modular components for the IPCC chapter processing pipeline.
Each component is designed to be configurable and reusable.
"""

__version__ = "1.0.0"
__author__ = "IPCC Pipeline Team"

from .downloader import WebDownloader
from .cleaner import ContentCleaner
from .structurer import ContentStructurer
from .chunker import ContentChunker
from .dictionary import DictionaryExtractor
from .encyclopedia import EncyclopediaBuilder
from .quality import QualityChecker

__all__ = [
    'WebDownloader',
    'ContentCleaner', 
    'ContentStructurer',
    'ContentChunker',
    'DictionaryExtractor',
    'EncyclopediaBuilder',
    'QualityChecker'
] 