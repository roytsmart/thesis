import pathlib

import numpy as np
import pylatex
import pymupdf
import pytest

import thesis


def test_document(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    doc = thesis.document(manuscripts=manuscripts, root=root)
    assert isinstance(doc, pylatex.Document)

    tex = doc.dumps()
    assert tex.startswith(r"\DocumentMetadata")
    assert r"\documentclass[dissertation]{MSUstyle}" in tex
    assert r"\nocite{Doe2020,first2021,second2021}" in tex
    assert tex.count(r"\includemanuscript[") == len(manuscripts)


def _margins(page: pymupdf.Page) -> tuple[float, float, float, float]:
    """
    The blank margins of a page, measured from its pixels, in inches.

    Parameters
    ----------
    page
        The page to measure.

    Returns
    -------
        The left, right, top, and bottom margins.
    """
    pixmap = page.get_pixmap(dpi=144, colorspace=pymupdf.csGRAY)
    pixels = np.frombuffer(pixmap.samples, dtype=np.uint8)
    pixels = pixels.reshape(pixmap.height, pixmap.width)
    rows, columns = np.nonzero(pixels < 250)
    return (
        columns.min() / 144,
        (pixmap.width - columns.max() - 1) / 144,
        rows.min() / 144,
        (pixmap.height - rows.max() - 1) / 144,
    )


def _number(page: pymupdf.Page) -> int:
    """
    The page number of the thesis printed on a page, which is the number at
    the center of its header.

    Parameters
    ----------
    page
        The page to read the number from.
    """
    (word,) = [
        word
        for word in page.get_text("words")
        if word[3] < 1.25 * 72
        and abs((word[0] + word[2]) / 2 - page.rect.width / 2) < 20
    ]
    return int(word[4])


@pytest.fixture
def pdf(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
    tmp_path: pathlib.Path,
) -> pathlib.Path:
    """
    The thesis, built from the manuscripts written by the fixture.
    """
    return thesis.pdf(
        manuscripts=manuscripts,
        root=root,
        directory=tmp_path / "build",
    )


def test_pdf(
    pdf: pathlib.Path,
    manuscripts: list[thesis.Manuscript],
) -> None:
    assert pdf.exists()

    with pymupdf.open(pdf) as document:
        text = [page.get_text() for page in document]
        toc = document.get_toc(simple=True)

        # Each manuscript is the three pages of its PDF, after its
        # Contribution of Authors and Co-Authors and Manuscript Information
        # pages.
        pages = [
            i
            for i, page in enumerate(text)
            if "Manuscript Information" in page and "Status of Manuscript" in page
        ]
        assert len(pages) == len(manuscripts)

        for page in pages:
            for i in range(page + 1, page + 4):
                left, right, _, bottom = _margins(document[i])

                # The Graduate School asks for margins of at least an inch.
                assert left > 1 - 0.02
                assert right > 1 - 0.02
                assert bottom > 1 - 0.02

                # The page numbers of the thesis continue through the pages
                # of the manuscript.
                assert _number(document[i]) == _number(document[i - 1]) + 1

    # Every reference cited by the manuscripts is in the cumulative
    # references.
    assert "A Work Cited by Every Manuscript" in text[-1]
    assert "A Work Cited by the First Manuscript" in text[-1]
    assert "A Work Cited by the Second Manuscript" in text[-1]

    # The headings of each manuscript are in the table of contents.
    titles = [title for _, title, _ in toc]
    for manuscript in manuscripts:
        index = next(i for i, title in enumerate(titles) if manuscript.title in title)
        assert titles[index + 1 : index + 9] == [
            "Contribution of Authors and Co-Authors",
            "Manuscript Information",
            "Abstract",
            "Introduction",
            "The Details",
            "The Finer Details",
            "An Appendix",
            "References",
        ]

    # Every cross-reference resolved.
    assert all("??" not in page for page in text)
