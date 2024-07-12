import re
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """

    entries_dir = os.path.join(os.path.dirname(__file__), 'entries')
    if not default_storage.exists(entries_dir):
        return []
    
    _, filenames = default_storage.listdir(entries_dir)
    return list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))

def get_entry(entry_name):
    """
    Retrieves the content of a specific encyclopedia entry by name.
    """
    entry_path = os.path.join(os.path.dirname(__file__), 'entries', f'{entry_name}.md')
    print(f"Path to entry file: {entry_path}")  # Print the path for debugging
    if not default_storage.exists(entry_path):
        return None
    
    with default_storage.open(entry_path, 'r') as file:
        content = file.read()
    
    return content