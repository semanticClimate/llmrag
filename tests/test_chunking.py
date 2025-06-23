import unittest
from pathlib import Path

from lxml.html import HTMLParser

from llmrag.chunking import split_documents
from lxml import etree as ET

class TestChunking(unittest.TestCase):
    def test_split_documents(self):
        text = "abcdefghijklmnopqrstuvwxyz"
        chunks = split_documents(text, chunk_size=10, overlap=2)
        self.assertEqual(chunks[0], "abcdefghij")
        self.assertEqual(chunks[1][:2], "ij")  # Overlap check

    def test_split_html_with_ids(self):
        """
        customise this to extract chunks out of YOUR chapter
        (mine was wg1/chapter04)
        Returns
        -------

        """
        test_dir = Path("tests", "ipcc")
        assert test_dir.exists(), f"{test_dir} should exist"
        wg = "wg1"
        chapter = "chapter04"
        div_id = "4.1"
        p_count = 12
        chunks = self.create_chunks(test_dir, wg, chapter, div_id, p_count)
        for chunk in chunks:
            print(f"{len(chunk)}: {chunk[:200]}")

    def create_chunks(self, dir, wg, chapter, div_id, p_count=None):
        """

        Parameters
        ----------
        dir top of ipcc tree (normally tests/ipcc)
        wg working group as wg1 etc
        chapter as chapter03 etc
        div_id e.g. "4.1" etc
        p_count predicted count of paragraphs

        Returns
        -------
        list of paragraph text chunks
        """
        chap_html = Path(dir, wg, chapter, "html_with_ids.html")
        assert chap_html.exists(), f"chapter {chap_html} should exist"
        htmlx = ET.parse(chap_html, HTMLParser())
        assert htmlx is not None
        div = htmlx.find(f".//div[@id='{div_id}']")
        assert div is not None
        paras = div.findall("./div/p[@id]")
        if p_count:
            assert (n := len(paras)) == p_count, f"expected {p_count} paras, found {n}"
        chunks = []
        for para in paras:
            text = " ".join(para.itertext())
            chunks.append(text)
        return chunks
