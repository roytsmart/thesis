import pathlib

import pymupdf
import pytest

import thesis

linenumbers_per_page = 50
"""How many lines are numbered on each page of a manuscript with line numbers."""


def _manuscript(
    directory: pathlib.Path,
    name: str,
    linenumbers: bool = False,
) -> thesis.Manuscript:
    """
    Write a small manuscript into a directory, as
    :meth:`thesis.Manuscript.download` would, and describe it.

    The PDF has three letter-sized pages whose layout spans from 50 to 562
    big points across and from 40 to 752 big points down, marked by a black
    square in its top left and bottom right corners, an abstract and a list
    of references which are not bookmarked, and a bookmark for an appendix
    which points to the first page instead of the third, as the bookmarks of
    an appendix sometimes do.

    Every manuscript cites the same work, but only the one named ``first``
    spells its key ``Doe2020``, the others spelling it ``doe2020``, since
    BibTeX stops at two citations whose keys differ only in case.

    Parameters
    ----------
    directory
        The directory holding the directories of every manuscript.
    name
        The name of the manuscript.
    linenumbers
        Whether to number the lines of the manuscript, as a draft for review
        does, in the margin to the left of the layout, with the numbers right
        aligned at 40 big points.
    """
    manuscript = thesis.Manuscript(
        name=name,
        title=f"The {name.title()} Manuscript",
        authors=[
            thesis.Author("Roy T. Smart", contributions="Wrote the manuscript."),
            thesis.Author("Charles C. Kankelborg"),
        ],
        stem=f"{name}-article",
        repository=f"https://github.com/roytsmart/{name}",
        url=f"https://roytsmart.github.io/{name}/",
        layout=thesis.Layout(left=50, top=40, right=562, bottom=752),
    )

    path = manuscript.pdf(directory)
    path.parent.mkdir(parents=True, exist_ok=True)

    document = pymupdf.open()
    for _ in range(3):
        page = document.new_page(width=612, height=792)
        page.draw_rect(pymupdf.Rect(50, 40, 60, 50), color=None, fill=(0, 0, 0))
        page.draw_rect(pymupdf.Rect(552, 742, 562, 752), color=None, fill=(0, 0, 0))
    document[0].insert_text((100, 100), "Abstract", fontsize=10)
    document[0].insert_text((100, 200), "1. Introduction", fontsize=10)
    document[1].insert_text((100, 100), "1.1. The Details", fontsize=10)
    document[1].insert_text((100, 200), "1.1.1. The Finer Details", fontsize=10)
    document[1].insert_text((100, 300), "1.1.1.1. Too Fine", fontsize=10)
    document[2].insert_text((100, 100), "Appendix A. An Appendix", fontsize=10)
    document[2].insert_text((100, 200), "REFERENCES", fontsize=10)
    document[2].insert_text((100, 220), "Doe, J. 2020, ApJ, 1, 1", fontsize=10)
    document.set_toc(
        [
            [1, "Introduction", 1],
            [2, "The Details", 2],
            [3, "The Finer Details", 2],
            [4, "Too Fine", 2],
            [1, "An Appendix", 1],
        ]
    )
    if linenumbers:
        number = 1
        for page in document:
            for i in range(linenumbers_per_page):
                text = str(number)
                width = pymupdf.get_text_length(text, fontname="helv", fontsize=5)
                page.insert_text((40 - width, 60 + 13 * i), text, fontsize=5)
                number += 1
    document.save(path)
    document.close()

    doe = "Doe2020" if name == "first" else "doe2020"

    manuscript.bbl(directory).write_text(
        "\\begin{thebibliography}{}\n"
        f"\\bibitem[{{{{Doe}}(2020)}}]{{{doe}}}\n"
        "{Doe}, J. 2020, \\apj, 1, 1\n"
        f"\\bibitem[{{{{Roe}}(2021)}}]{{{name}2021}}\n"
        "{Roe}, R. 2021, \\solphys, 2, 2\n"
        "\\end{thebibliography}\n",
        encoding="utf-8",
    )
    manuscript.bib(directory).write_text(
        f"@article{{{doe},\n"
        "  author = {{Doe}, J.},\n"
        "  title = {A Work Cited by Every Manuscript},\n"
        "  journal = {\\apj},\n"
        "  year = {2020},\n"
        "  volume = {1},\n"
        "  pages = {1},\n"
        "}\n\n"
        f"@article{{{name}2021,\n"
        "  author = {{Roe}, R.},\n"
        f"  title = {{A Work Cited by the {name.title()} Manuscript}},\n"
        "  journal = {\\solphys},\n"
        "  year = {2021},\n"
        "  volume = {2},\n"
        "  pages = {2},\n"
        "}\n",
        encoding="utf-8",
    )

    return manuscript


@pytest.fixture
def root(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    A temporary directory to write the manuscripts into.
    """
    return tmp_path / "manuscripts"


@pytest.fixture
def manuscripts(root: pathlib.Path) -> list[thesis.Manuscript]:
    """
    Two small manuscripts written into :func:`root`, the same but for the
    line numbers of the second.
    """
    return [
        _manuscript(root, "first"),
        _manuscript(root, "second", linenumbers=True),
    ]
