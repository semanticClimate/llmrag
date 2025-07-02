#!/usr/bin/env python3
"""
Test script for the IPCC Pipeline

This script demonstrates the pipeline functionality with a simple example.
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ipcc_pipeline import IPCCPipeline, PipelineConfig


def test_pipeline():
    """Test the pipeline with a simple configuration."""
    
    # Create a minimal test configuration
    test_config = {
        'pipeline': {
            'name': 'Test IPCC Pipeline',
            'version': '1.0'
        },
        'sources': [
            {
                'name': 'test_chapter',
                'url': 'https://example.com',
                'working_group': 'wg1',
                'chapter': 'chapter01'
            }
        ],
        'stages': {
            'download': {'enabled': False},  # Skip download for test
            'clean': {'enabled': True, 'extractors': ['readability'], 'cleaners': []},
            'structure': {'enabled': True, 'add_paragraph_ids': True},
            'chunk': {'enabled': False},
            'dictionary': {'enabled': False},
            'encyclopedia': {'enabled': False}
        },
        'quality_checks': [],
        'error_handling': {'continue_on_error': True}
    }
    
    # Write test config to file
    config_path = Path('test_config.yaml')
    import yaml
    with open(config_path, 'w') as f:
        yaml.dump(test_config, f)
    
    # Create test HTML content
    test_html = """
    <html>
    <head><title>Test Chapter</title></head>
    <body>
        <h1>Introduction</h1>
        <p>This is a test paragraph about climate change.</p>
        <h2>Background</h2>
        <p>Another paragraph with important information.</p>
        <p>Third paragraph with more details.</p>
    </body>
    </html>
    """
    
    # Write test HTML to file
    test_html_path = Path('test_input.html')
    test_html_path.write_text(test_html)
    
    print("Test configuration created:")
    print(f"- Config file: {config_path}")
    print(f"- Test HTML: {test_html_path}")
    print("\nTo run the pipeline:")
    print(f"python ipcc_pipeline.py --config {config_path} --source test_chapter")


if __name__ == "__main__":
    test_pipeline() 