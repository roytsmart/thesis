"""
Assemble the thesis from its chapters and manuscripts, and compile it.
"""

from . import chapters
from ._document import Document, directory_build, document, pdf
from ._front import abstract, front
from ._layout import Layout, aastex_twocolumn, spieman
from ._manuscripts import Author, Manuscript, directory_manuscripts, manuscripts
from ._pages import Heading, headings
from ._preamble import preamble
from ._references import bibliography, citations

__all__ = [
    "Author",
    "Document",
    "Heading",
    "Layout",
    "Manuscript",
    "aastex_twocolumn",
    "abstract",
    "bibliography",
    "chapters",
    "citations",
    "directory_build",
    "directory_manuscripts",
    "document",
    "front",
    "headings",
    "manuscripts",
    "pdf",
    "preamble",
    "spieman",
]
