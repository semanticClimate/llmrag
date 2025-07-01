import unittest
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSimple(unittest.TestCase):
    """Very simple tests that should always pass."""

    def test_python_version(self):
        """Test that we're running on a compatible Python version."""
        self.assertGreaterEqual(sys.version_info, (3, 8))

    def test_basic_math(self):
        """Test that basic math works."""
        self.assertEqual(2 + 2, 4)
        self.assertTrue(True)

    def test_string_operations(self):
        """Test that string operations work."""
        text = "Hello, World!"
        self.assertIn("Hello", text)
        self.assertEqual(len(text), 13)

    def test_list_operations(self):
        """Test that list operations work."""
        items = [1, 2, 3, 4, 5]
        self.assertEqual(len(items), 5)
        self.assertEqual(sum(items), 15)

    def test_dict_operations(self):
        """Test that dictionary operations work."""
        data = {"key": "value", "number": 42}
        self.assertEqual(data["key"], "value")
        self.assertEqual(data["number"], 42)


if __name__ == "__main__":
    unittest.main() 