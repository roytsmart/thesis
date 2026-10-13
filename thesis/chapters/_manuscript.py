import pathlib

import pylatex
import pylatex.utils
import pymupdf

import thesis

from ._chapter import Chapter

__all__ = [
    "manuscript",
]

_statuses = {
    "prepared": "Prepared for submission to a peer-reviewed journal",
    "submitted": "Officially submitted to a peer-reviewed journal",
    "accepted": "Accepted by a peer-reviewed journal",
    "published": "Published in a peer-reviewed journal",
}

_sections = {
    1: "section",
    2: "subsection",
    3: "subsubsection",
}

_newline = "\\\\\n"
"""The LaTeX for a line break, followed by a newline in the source."""


def _names(authors: "list[thesis.Author]") -> str:
    """
    The names of the authors of a manuscript, joined into a list.

    Parameters
    ----------
    authors
        The authors of the manuscript.
    """
    names = [pylatex.utils.escape_latex(author.name) for author in authors]
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


def _contributions(manuscript: "thesis.Manuscript") -> pylatex.Section:
    """
    The Contribution of Authors and Co-Authors page of a manuscript, which
    lists every author with a brief paragraph of what they contributed.

    Parameters
    ----------
    manuscript
        The manuscript the page describes.
    """
    result = pylatex.Section(
        pylatex.NoEscape("Contribution of Authors and Co-Authors"),
        label=False,
    )
    result.append(
        pylatex.NoEscape(
            rf"\noindent Manuscript in Chapter~\ref{{chapter:{manuscript.name}}}"
        )
    )
    for i, author in enumerate(manuscript.authors):
        role = "Author" if i == 0 else "Co-Author"
        contributions = author.contributions
        if contributions is None:
            contributions = r"\textbf{XX}"
        result.append(pylatex.NoEscape(rf"""

\begin{{singlespace}}
\noindent {role}: {pylatex.utils.escape_latex(author.name)}

\noindent Contributions: {contributions}
\end{{singlespace}}"""))
    return result


def _information(manuscript: "thesis.Manuscript") -> pylatex.Section:
    """
    The Manuscript Information page of a manuscript, which gives its authors
    and how far it is through peer review.

    Parameters
    ----------
    manuscript
        The manuscript the page describes.
    """
    result = pylatex.Section("Manuscript Information", label=False)
    result.append(pylatex.NoEscape(rf"\noindent {_names(manuscript.authors)}"))

    if manuscript.journal is not None:
        journal = pylatex.utils.escape_latex(manuscript.journal)
        result.append(pylatex.NoEscape(rf"""

\noindent \textit{{{journal}}}"""))

    boxes = []
    for status, text in _statuses.items():
        box = r"\boxtimes" if status == manuscript.status else r"\square"
        boxes.append(rf"${box}$ {text}")
    boxes = _newline.join(boxes)
    result.append(pylatex.NoEscape(rf"""

\begin{{singlespace}}
\noindent Status of Manuscript:\\
{boxes}
\end{{singlespace}}"""))

    details = [
        manuscript.publisher,
        manuscript.submitted,
        manuscript.appears,
        manuscript.issue,
        None if manuscript.doi is None else f"DOI: {manuscript.doi}",
    ]
    details = [pylatex.utils.escape_latex(d) for d in details if d is not None]
    if details:
        details = _newline.join(details)
        result.append(pylatex.NoEscape(rf"""

\begin{{singlespace}}
\noindent {details}
\end{{singlespace}}"""))

    return result


def manuscript(
    manuscript: "thesis.Manuscript",
    path: pathlib.Path,
    name: str,
) -> Chapter:
    """
    The chapter of the thesis holding a manuscript.

    Following the Scholarly Works Option of the Graduate School, the chapter
    begins with the Contribution of Authors and Co-Authors and the
    Manuscript Information pages, after which come the pages of the
    manuscript itself, formatted as the journal formats them, with the
    :class:`thesis.Layout` of the journal fit into the text block.
    The headings of the manuscript are listed in the table of contents of the
    thesis, as the Graduate School asks.

    Parameters
    ----------
    manuscript
        The manuscript to include.
    path
        The PDF of the manuscript, which is read to find its headings.
    name
        The name the PDF of the manuscript is included by, relative to the
        directory the thesis is built in.
    """
    layout = manuscript.layout
    with pymupdf.open(path) as document:
        sizes = {(round(page.rect.width), round(page.rect.height)) for page in document}
    if sizes != {(round(layout.width), round(layout.height))}:
        raise ValueError(
            f"the pages of {path} are {sizes} big points, but the layout of "
            f"{manuscript.name!r} is for pages of {layout.width} by "
            f"{layout.height} big points."
        )

    label = pylatex.Label(pylatex.Marker(manuscript.name, prefix="chapter"))
    result = Chapter(manuscript.title, label=label)

    result.append(_contributions(manuscript))
    result.append(pylatex.NoEscape(r"\clearpage"))
    result.append(_information(manuscript))

    trim = " ".join(f"{t:.2f}bp" for t in layout.trim)
    options = [f"trim={trim}"]

    entries = [
        f"{heading.page},{_sections[heading.level]},{heading.level},"
        f"{{{pylatex.utils.escape_latex(heading.title)}}},"
        f"{manuscript.name}:{i}"
        for i, heading in enumerate(thesis.headings(path))
    ]
    if entries:
        options.append(f"addtotoc={{{','.join(entries)}}}")

    result.append(
        pylatex.NoEscape(rf"\includemanuscript[{','.join(options)}]{{{name}}}")
    )

    return result
