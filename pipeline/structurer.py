"""
Content Structurer Component

Adds semantic paragraph IDs to HTML content for source tracking.
Supports hierarchical ID generation algorithms.
"""

import logging
from typing import Dict, Any, List
from lxml import html, etree
import re


class ContentStructurer:
    """
    Adds semantic structure and paragraph IDs to HTML content.
    
    Supports different ID generation algorithms for source tracking.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.id_counter = 0
        
    def structure(self, html_content: str) -> str:
        """
        Add structure and paragraph IDs to HTML content.
        
        Args:
            html_content: Cleaned HTML content
            
        Returns:
            HTML content with added paragraph IDs
        """
        tree = html.fromstring(html_content)
        
        # Add paragraph IDs
        if self.config.get('add_paragraph_ids', True):
            tree = self._add_paragraph_ids(tree)
        
        # Preserve headings and lists
        if self.config.get('preserve_headings', True):
            tree = self._preserve_headings(tree)
        
        if self.config.get('preserve_lists', True):
            tree = self._preserve_lists(tree)
        
        return etree.tostring(tree, encoding='unicode', pretty_print=True)
    
    def _add_paragraph_ids(self, tree) -> etree._Element:
        """Add semantic paragraph IDs to the document."""
        algorithm = self.config.get('id_algorithm', 'semantic_hierarchical')
        id_format = self.config.get('id_format', '{section}_{subsection}_{paragraph}')
        
        if algorithm == 'semantic_hierarchical':
            return self._add_hierarchical_ids(tree, id_format)
        elif algorithm == 'sequential':
            return self._add_sequential_ids(tree)
        else:
            self.logger.warning(f"Unknown ID algorithm: {algorithm}")
            return self._add_sequential_ids(tree)
    
    def _add_hierarchical_ids(self, tree, id_format: str) -> etree._Element:
        """Add hierarchical paragraph IDs based on document structure."""
        current_section = "main"
        current_subsection = "content"
        paragraph_counter = 1
        
        # Find all content elements (headings, paragraphs, lists)
        content_elements = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //p | //ul | //ol | //li')
        
        for element in content_elements:
            tag = element.tag
            
            # Update section based on headings
            if tag.startswith('h'):
                level = int(tag[1])
                heading_text = element.text_content().strip()
                
                if level == 1:
                    current_section = self._normalize_id(heading_text)
                    current_subsection = "content"
                    paragraph_counter = 1
                elif level == 2:
                    current_subsection = self._normalize_id(heading_text)
                    paragraph_counter = 1
                elif level == 3:
                    current_subsection = self._normalize_id(heading_text)
                    paragraph_counter = 1
                
                # Add ID to heading
                element.set('id', f"{current_section}_{current_subsection}_heading")
            
            # Add ID to paragraphs and list items
            elif tag in ['p', 'li']:
                if tag == 'p':
                    # Generate paragraph ID
                    paragraph_id = id_format.format(
                        section=current_section,
                        subsection=current_subsection,
                        paragraph=f"p{paragraph_counter}"
                    )
                    element.set('id', paragraph_id)
                    paragraph_counter += 1
                else:
                    # Generate list item ID
                    list_id = f"{current_section}_{current_subsection}_li{paragraph_counter}"
                    element.set('id', list_id)
                    paragraph_counter += 1
        
        return tree
    
    def _add_sequential_ids(self, tree) -> etree._Element:
        """Add sequential paragraph IDs."""
        counter = 1
        
        for element in tree.xpath('//p | //li'):
            element.set('id', f"paragraph_{counter}")
            counter += 1
        
        return tree
    
    def _normalize_id(self, text: str) -> str:
        """Normalize text to create valid HTML IDs."""
        # Convert to lowercase
        normalized = text.lower()
        
        # Replace spaces and special characters with underscores
        normalized = re.sub(r'[^a-z0-9]+', '_', normalized)
        
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        
        # Ensure it starts with a letter
        if normalized and not normalized[0].isalpha():
            normalized = f"section_{normalized}"
        
        return normalized or "section"
    
    def _preserve_headings(self, tree) -> etree._Element:
        """Ensure headings are preserved and properly structured."""
        # This is mainly for validation - headings should already be preserved
        # from the cleaning stage
        return tree
    
    def _preserve_lists(self, tree) -> etree._Element:
        """Ensure lists are preserved and properly structured."""
        # This is mainly for validation - lists should already be preserved
        # from the cleaning stage
        return tree 