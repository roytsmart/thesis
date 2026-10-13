import dataclasses
import pathlib
import re

import numpy as np
import pymupdf

__all__ = [
    "Heading",
    "headings",
    "trim",
]


def trim(
    path: pathlib.Path,
    resolution: float = 144,
    threshold: int = 250,
    padding: float = 1,
) -> tuple[float, float, float, float]:
    """
    How much of each edge of the pages of a PDF is blank.

    The pages are rendered and the blank margin is measured from the pixels,
    rather than from the objects on the page, since a figure often draws
    shapes which its clipping path hides.
    The margins are the smallest over every page of the document, so that
    trimming all of the pages by them cuts nothing off any of them.

    Parameters
    ----------
    path
        The PDF to measure.
    resolution
        The resolution to render the pages at, in dots per inch.
    threshold
        The gray level, out of 255, below which a pixel counts as ink.
    padding
        A margin of blank space to keep around the ink, in big points.

    Returns
    -------
        The blank margin on the left, bottom, right, and top of the pages,
        in big points, in the order that the ``trim`` option of
        ``\\includegraphics`` expects.
    """
    left = bottom = right = top = np.inf

    with pymupdf.open(path) as document:
        for page in document:
            pixmap = page.get_pixmap(dpi=resolution, colorspace=pymupdf.csGRAY)
            pixels = np.frombuffer(pixmap.samples, dtype=np.uint8)
            pixels = pixels.reshape(pixmap.height, pixmap.width)
            rows, columns = np.nonzero(pixels < threshold)
            if rows.size == 0:
                continue

            scale = 72 / resolution
            width = page.rect.width
            height = page.rect.height

            left = min(left, columns.min() * scale)
            right = min(right, width - (columns.max() + 1) * scale)
            top = min(top, rows.min() * scale)
            bottom = min(bottom, height - (rows.max() + 1) * scale)

    if np.isinf(left):
        raise ValueError(f"every page of {path} is blank")

    def _pad(margin: float) -> float:
        return round(max(margin - padding, 0), 1)

    return _pad(left), _pad(bottom), _pad(right), _pad(top)


@dataclasses.dataclass
class Heading:
    """
    A heading of a manuscript, as listed in the table of contents of the
    thesis.
    """

    level: int
    """The depth of the heading, where ``1`` is a section."""

    title: str
    """The text of the heading."""

    page: int
    """The page of the manuscript the heading is on, counting from one."""


def _squash(text: str) -> str:
    """
    Remove the whitespace and case from some text, so that a heading can be
    found on a page however its words were broken across lines.

    Parameters
    ----------
    text
        The text to normalize.
    """
    return re.sub(r"\s+", "", text).casefold()


def headings(
    path: pathlib.Path,
    depth: int = 3,
) -> list[Heading]:
    """
    The headings of a manuscript, from the bookmarks of its PDF.

    The Graduate School asks for the first-, second-, and third-level
    headings of every manuscript to appear in the table of contents of the
    thesis, as they would for any other chapter.
    The bookmarks which ``hyperref`` writes are the headings of the article,
    but a bookmark sometimes points at the wrong page, as one in an appendix
    does when its anchor has the same name as one in the body.
    So each heading is looked for on the page its bookmark points to, and
    otherwise on the pages after the heading before it.

    The abstract and the references are usually not bookmarked, so they are
    added if the manuscript has them.

    Parameters
    ----------
    path
        The PDF of the manuscript.
    depth
        The deepest level of heading to include.
    """
    with pymupdf.open(path) as document:
        pages = [_squash(page.get_text()) for page in document]
        lines = [
            [line.strip().casefold() for line in page.get_text().splitlines()]
            for page in document
        ]
        bookmarks = document.get_toc(simple=True)

    result = []
    page_previous = 1
    for level, title, page in bookmarks:
        if level > depth:
            continue
        page = min(max(page, 1), len(pages))
        squashed = _squash(title)
        if squashed not in pages[page - 1] or page < page_previous:
            candidates = [
                p
                for p in range(page_previous, len(pages) + 1)
                if squashed in pages[p - 1]
            ]
            if candidates:
                page = candidates[0]
            else:
                page = max(page, page_previous)
        result.append(Heading(level=level, title=title, page=page))
        page_previous = page

    titles = {_squash(heading.title) for heading in result}

    if "abstract" not in titles and "abstract" in pages[0]:
        result.insert(0, Heading(level=1, title="Abstract", page=1))

    if "references" not in titles:
        pages_references = [
            p + 1 for p, page in enumerate(lines) if "references" in page
        ]
        if pages_references:
            heading = Heading(level=1, title="References", page=pages_references[-1])
            index = len(result)
            while index > 0 and result[index - 1].page > heading.page:
                index -= 1
            result.insert(index, heading)

    return result
