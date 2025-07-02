import yaml
from langchain_core.documents import Document

def load_paragraphs_yaml(path):
    """
    Loads a YAML file containing paragraphs with metadata.

    Args:
        path (str): Path to the YAML file.

    Returns:
        List[Document]: List of Document instances.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return [Document(page_content=entry["text"], metadata={"id": entry["id"]}) for entry in data]
