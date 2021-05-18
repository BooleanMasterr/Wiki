import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings


def list_entries():
    """
    Returns a list of all names of encyclopedia6 entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def get_example(title):
    try:
        f = default_storage.open(f"entries/examples/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def list_example():
    _, filenames = default_storage.listdir("entries/examples")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def is_sub_str(sub_str):
    """
    Returns recommendations based on what
    the user has entered in the search field
    """

    for entry in list_entries():

        entry = str(entry)

        if entry.lower().find(sub_str.lower()) == -1:
            continue
        else:
            return entry
