import re
import os
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """

    entries_dir = os.path.join(os.path.dirname(__file__), '../entries')
    if not default_storage.exists(entries_dir):
        return []
    
    _, filenames = default_storage.listdir(entries_dir)
    return list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))

def get_random_entry():
    """
    Returns a random name of an encyclopedia entry.
    """

    entries_dir = os.path.join(os.path.dirname(__file__), '../entries')
    
    if not default_storage.exists(entries_dir):
        return None
    
    _, filenames = default_storage.listdir(entries_dir)
    entries = [re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")]
    
    if entries:
        return random.choice(entries)
    return None

def modif_file(filename, content):
    """ 
    Modify a entry file passing this name and it's new content
    """

    entries_dir = os.path.join(os.path.dirname(__file__), '../entries')
    filepath = os.path.join(entries_dir, f"{filename}.md")
    with default_storage.open(filepath, 'w') as file:
        file.truncate(0)
        file.write(content)
        file.close()

def get_entry(entry_name):
    """
    Retrieves the content of a specific encyclopedia entry by name.
    """

    entry_path = os.path.join(os.path.dirname(__file__), '../entries', f'{entry_name}.md')
    if not default_storage.exists(entry_path):
        return None
    with default_storage.open(entry_path, 'r') as file:
        content = file.read()
    
    return content

def create_entry(filename, content):
    """
    Creates a new encyclopedia entry with the given filename and content.
    The file will be saved as a .md file.
    """
    entries_dir = os.path.join(os.path.dirname(__file__), '../entries')
    
    if not default_storage.exists(entries_dir):
        default_storage.makedirs(entries_dir)
    
    filepath = os.path.join(entries_dir, f"{filename}.md")
    
    with default_storage.open(filepath, 'w') as file:
        file.write(content)
