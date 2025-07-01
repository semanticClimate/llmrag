# IPCC Chapter Processing Pipeline

A declarative pipeline for downloading, cleaning, and enriching IPCC chapters with semantic paragraph IDs and encyclopedia generation.

## Features

- **Declarative Configuration**: YAML-based configuration for easy customization
- **Modular Design**: Each stage can be enabled/disabled independently
- **Multiple Extraction Methods**: Support for Readability, Trafilatura, and Selenium
- **Semantic Paragraph IDs**: Hierarchical ID generation for source tracking
- **Content Cleaning**: Removes ads, navigation, and styling markup
- **Dictionary Extraction**: Extracts significant terms from chapters
- **Encyclopedia Generation**: Wikipedia integration for term definitions and images
- **Quality Checks**: Automated validation of processed content

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r pipeline_requirements.txt
   ```

2. **Create Configuration**:
   ```bash
   python test_pipeline.py
   ```

3. **Run Pipeline**:
   ```bash
   python ipcc_pipeline.py --config pipeline_config.yaml --source wg1_chapter02
   ```

## Configuration

The pipeline is configured via YAML files. Key sections:

### Sources
Define the IPCC chapters to process:
```yaml
sources:
  - name: "wg1_chapter02"
    url: "https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-2/"
    working_group: "wg1"
    chapter: "chapter02"
    expected_title: "Changing State of the Climate System"
```

### Stages
Configure each processing stage:
```yaml
stages:
  download:
    enabled: true
    method: "selenium_headless"
    wait_time: 5
    
  clean:
    enabled: true
    extractors: ["readability", "trafilatura"]
    cleaners: ["remove_ads", "clean_gatsby_markup"]
    
  structure:
    enabled: true
    add_paragraph_ids: true
    id_algorithm: "semantic_hierarchical"
```

## Pipeline Stages

### 1. Download
- Downloads HTML content from IPCC URLs
- Supports Selenium for JavaScript-heavy sites
- Configurable wait times and retry logic

### 2. Clean
- Extracts main content using Readability/Trafilatura
- Removes ads, navigation, footers
- Cleans Gatsby and WordPress markup

### 3. Structure
- Adds semantic paragraph IDs
- Supports hierarchical ID generation
- Preserves document structure

### 4. Chunk
- Splits content into RAG-friendly chunks
- Preserves paragraph IDs
- Configurable chunk size and overlap

### 5. Dictionary
- Extracts significant terms using NLP
- Supports named entity recognition
- Domain-specific climate terms

### 6. Encyclopedia
- Wikipedia lookups for terms
- Image downloads
- Creates mini-encyclopedia

## Usage Examples

### Process Single Chapter
```bash
python ipcc_pipeline.py --config pipeline_config.yaml --source wg1_chapter02
```

### Process All Chapters
```bash
python ipcc_pipeline.py --config pipeline_config.yaml --all
```

### Custom Output Directory
```bash
python ipcc_pipeline.py --config pipeline_config.yaml --source wg1_chapter02 --output-dir ./my_output
```

## Output Structure

```
output/
├── wg1/
│   └── chapter02/
│       ├── raw.html              # Downloaded content
│       ├── cleaned.html          # Cleaned content
│       ├── structured.html       # Content with paragraph IDs
│       ├── chunks.json           # RAG chunks
│       ├── dictionary.json       # Extracted terms
│       ├── encyclopedia.json     # Wikipedia data
│       └── quality_report.json   # Quality check results
└── pipeline.log                  # Pipeline logs
```

## Customization

### Adding New Cleaners
Extend the `ContentCleaner` class:
```python
def _clean_custom_markup(self, tree):
    # Your custom cleaning logic
    return tree
```

### Custom ID Algorithms
Implement new algorithms in `ContentStructurer`:
```python
def _add_custom_ids(self, tree):
    # Your custom ID generation
    return tree
```

### New Extraction Methods
Add extractors to the configuration:
```yaml
extractors:
  - "readability"
  - "trafilatura"
  - "custom_extractor"
```

## Dependencies

- **Core**: PyYAML, lxml, requests
- **Web Scraping**: Selenium, readability-lxml, trafilatura
- **NLP**: spaCy, keybert, transformers
- **Wikipedia**: wikipedia-api, wikipedia
- **Images**: Pillow

## Contributing

1. Follow the modular design pattern
2. Use absolute imports
3. Add comprehensive logging
4. Include error handling
5. Write tests for new components

## License

This project is part of the IPCC RAG system and follows the same licensing terms. 