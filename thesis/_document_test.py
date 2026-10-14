import dataclasses
import pathlib

import pylatex
import pymupdf
import pytest

import thesis

from .conftest import linenumbers_per_page


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


def test_document_page_size(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    a4 = thesis.Layout(left=50, top=40, right=545, bottom=802, width=595, height=842)
    manuscripts = [dataclasses.replace(manuscripts[0], layout=a4)]
    with pytest.raises(ValueError, match="layout"):
        thesis.document(manuscripts=manuscripts, root=root)


def _squares(page: pymupdf.Page) -> list[pymupdf.Rect]:
    """
    The black squares which mark the corners of the layout of a manuscript
    written by the fixture, from the top of the page down.

    Parameters
    ----------
    page
        A page of the thesis holding a page of the manuscript.
    """
    rects = [
        drawing["rect"]
        for drawing in page.get_drawings()
        if drawing.get("fill") == (0.0, 0.0, 0.0)
    ]
    return sorted(rects, key=lambda rect: rect.y0)


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
        first, second = pages

        for page in pages:
            for i in range(page + 1, page + 4):
                top_left, bottom_right = _squares(document[i])

                # The layout of the manuscript is inside the margins of an
                # inch which the Graduate School asks for.
                width = document[i].rect.width
                height = document[i].rect.height
                assert top_left.x0 > 72 - 0.1
                assert bottom_right.x1 < width - 72 + 0.1
                assert bottom_right.y1 < height - 72 + 0.1

                # The page numbers of the thesis continue through the pages
                # of the manuscript.
                assert _number(document[i]) == _number(document[i - 1]) + 1

        for i, j in zip(range(first + 1, first + 4), range(second + 1, second + 4)):
            # The line numbers of the second manuscript do not change its
            # scale, so a draft looks as its final version will.
            for a, b in zip(_squares(document[i]), _squares(document[j])):
                assert tuple(a) == pytest.approx(tuple(b), abs=0.01)

            # The line numbers are in the margin, to the left of the layout,
            # and still on the page.
            left = _squares(document[j])[0].x0
            numbers = [
                word
                for word in document[j].get_text("words")
                if word[4].isdigit() and word[2] < left
            ]
            assert len(numbers) == linenumbers_per_page
            assert all(word[0] > 0 for word in numbers)

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
