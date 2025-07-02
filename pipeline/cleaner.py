"""
Content Cleaner Component

Cleans HTML content by removing ads, navigation, and styling markup.
Supports multiple extraction methods (Readability, Trafilatura).
"""

import logging
from typing import Dict, Any, List
from lxml import html, etree
import re

try:
    from readability import Document
    READABILITY_AVAILABLE = True
except ImportError:
    READABILITY_AVAILABLE = False

try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False


class ContentCleaner:
    """
    Cleans HTML content by removing unwanted elements and markup.
    
    Supports multiple extraction methods and cleaning strategies.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def clean(self, html_content: str) -> str:
        """
        Clean HTML content using configured extractors and cleaners.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Cleaned HTML content
        """
        # First, extract main content
        extracted_content = self._extract_content(html_content)
        
        # Then apply cleaning rules
        cleaned_content = self._apply_cleaners(extracted_content)
        
        return cleaned_content
    
    def _extract_content(self, html_content: str) -> str:
        """Extract main content using configured extractors."""
        extractors = self.config.get('extractors', ['readability'])
        
        for extractor in extractors:
            try:
                if extractor == 'readability' and READABILITY_AVAILABLE:
                    return self._extract_with_readability(html_content)
                elif extractor == 'trafilatura' and TRAFILATURA_AVAILABLE:
                    return self._extract_with_trafilatura(html_content)
                else:
                    self.logger.warning(f"Extractor {extractor} not available")
            except Exception as e:
                self.logger.warning(f"Failed to extract with {extractor}: {e}")
        
        # Fallback: return original content
        return html_content
    
    def _extract_with_readability(self, html_content: str) -> str:
        """Extract content using Readability."""
        doc = Document(html_content)
        return doc.summary()
    
    def _extract_with_trafilatura(self, html_content: str) -> str:
        """Extract content using Trafilatura."""
        extracted = trafilatura.extract(html_content, include_formatting=True)
        return extracted if extracted else html_content
    
    def _apply_cleaners(self, html_content: str) -> str:
        """Apply cleaning rules to HTML content."""
        cleaners = self.config.get('cleaners', [])
        
        # Parse HTML
        tree = html.fromstring(html_content)
        
        for cleaner in cleaners:
            if cleaner == 'remove_ads':
                tree = self._remove_ads(tree)
            elif cleaner == 'remove_navigation':
                tree = self._remove_navigation(tree)
            elif cleaner == 'remove_footers':
                tree = self._remove_footers(tree)
            elif cleaner == 'clean_gatsby_markup':
                tree = self._clean_gatsby_markup(tree)
            elif cleaner == 'clean_wordpress_markup':
                tree = self._clean_wordpress_markup(tree)
        
        return etree.tostring(tree, encoding='unicode', pretty_print=True)
    
    def _remove_ads(self, tree) -> etree._Element:
        """Remove advertisement elements."""
        # Common ad selectors
        ad_selectors = [
            '.ad', '.advertisement', '.ads', '.adsbygoogle',
            '[class*="ad-"]', '[id*="ad-"]', '[class*="ads-"]'
        ]
        
        for selector in ad_selectors:
            for element in tree.xpath(selector):
                if element.getparent() is not None:
                    element.getparent().remove(element)
        
        return tree
    
    def _remove_navigation(self, tree) -> etree._Element:
        """Remove navigation elements."""
        nav_selectors = [
            'nav', '.nav', '.navigation', '.menu', '.navbar',
            '.breadcrumb', '.breadcrumbs', '.pagination'
        ]
        
        for selector in nav_selectors:
            for element in tree.xpath(selector):
                if element.getparent() is not None:
                    element.getparent().remove(element)
        
        return tree
    
    def _remove_footers(self, tree) -> etree._Element:
        """Remove footer elements."""
        footer_selectors = [
            'footer', '.footer', '.site-footer', '.page-footer'
        ]
        
        for selector in footer_selectors:
            for element in tree.xpath(selector):
                if element.getparent() is not None:
                    element.getparent().remove(element)
        
        return tree
    
    def _clean_gatsby_markup(self, tree) -> etree._Element:
        """Remove Gatsby-specific markup."""
        # Remove Gatsby-specific classes and attributes
        gatsby_selectors = [
            '[class*="gatsby-"]', '[data-gatsby-*]',
            '.gatsby-highlight', '.gatsby-resp-image-wrapper'
        ]
        
        for selector in gatsby_selectors:
            for element in tree.xpath(selector):
                if element.getparent() is not None:
                    element.getparent().remove(element)
        
        return tree
    
    def _clean_wordpress_markup(self, tree) -> etree._Element:
        """Remove WordPress-specific markup."""
        # Remove WordPress-specific classes and attributes
        wp_selectors = [
            '[class*="wp-"]', '[id*="wp-"]',
            '.wp-block-*', '.wp-caption', '.wp-image-*'
        ]
        
        for selector in wp_selectors:
            for element in tree.xpath(selector):
                if element.getparent() is not None:
                    element.getparent().remove(element)
        
        return tree 