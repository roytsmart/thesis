import pathlib
import shutil

import aastex
import pylatex

import thesis

__all__ = [
    "Document",
    "directory_build",
    "document",
    "pdf",
]

directory_build = pathlib.Path(__file__).parent / "build"
"""The directory :func:`pdf` builds the thesis in."""


class Document(aastex.Document):
    """
    An :class:`aastex.Document` which declares the metadata of the PDF before
    its class, as the template of the Graduate School does, so that the PDF
    is tagged for screen readers.
    """

    metadata: str = r"\DocumentMetadata{lang=en, testphase={phase-II,graphic}}"
    """The command declaring the metadata of the PDF."""

    def dumps(self) -> str:
        return self.metadata + "%\n" + super().dumps()


def document(
    manuscripts: "None | list[thesis.Manuscript]" = None,
    root: None | pathlib.Path = None,
) -> Document:
    """
    An :mod:`aastex` representation of the thesis, on the class of the
    Graduate School.

    Parameters
    ----------
    manuscripts
        The manuscripts to include as chapters.
        If :obj:`None`, :func:`thesis.manuscripts` is used.
    root
        The directory which holds the downloaded manuscripts.
        If :obj:`None`, :obj:`thesis.directory_manuscripts` is used.
    """
    if manuscripts is None:
        manuscripts = thesis.manuscripts()
    if root is None:
        root = thesis.directory_manuscripts

    doc = Document(
        documentclass="MSUstyle",
        class_files=[
            pathlib.Path(__file__).parent / "MSUstyle.cls",
            "aasjournalv7.bst",
        ],
        bibliographystyle="aasjournalv7",
        document_options=["dissertation"],
        lmodern=False,
        textcomp=False,
        linenumbers=False,
    )

    doc.preamble += thesis.preamble()
    doc.preamble += thesis.front()

    doc.append(pylatex.NoEscape(r"\begin{preliminary}"))
    doc.append(pylatex.NoEscape(r"\contents"))
    doc.append(thesis.abstract())
    doc.append(pylatex.NoEscape(r"\end{preliminary}"))

    doc.append(thesis.chapters.introduction())
    doc.append(thesis.chapters.methodology())
    for manuscript in manuscripts:
        doc.append(
            thesis.chapters.manuscript(
                manuscript=manuscript,
                path=manuscript.pdf(root),
                name=f"manuscripts/{manuscript.name}.pdf",
            )
        )
    doc.append(thesis.chapters.conclusion())

    # The Graduate School asks for the references of every manuscript in the
    # cumulative references at the end of the thesis, so everything the
    # manuscripts cite is cited here too.
    # BibTeX stops at two citations whose keys differ only in case, which two
    # manuscripts can use for the same work, so the first spelling is kept,
    # as it is by `thesis.bibliography()`.
    keys = {}
    for manuscript in manuscripts:
        for key in thesis.citations(manuscript.bbl(root)):
            keys.setdefault(key.casefold(), key)
    keys = list(keys.values())
    if keys:
        doc.append(pylatex.NoEscape(rf"\nocite{{{','.join(keys)}}}"))

    doc.append(pylatex.NoEscape(r"\references"))
    doc.append(aastex.Bibliography("references"))

    return doc


def pdf(
    manuscripts: "None | list[thesis.Manuscript]" = None,
    root: None | pathlib.Path = None,
    directory: None | pathlib.Path = None,
) -> pathlib.Path:
    """
    Build a pdf version of :func:`document` and return the path of the
    document.

    The PDF of each manuscript is copied into the build directory, and the
    bibliographies of the manuscripts are merged with that of the thesis into
    ``references.bib`` there.

    Parameters
    ----------
    manuscripts
        The manuscripts to include as chapters.
        If :obj:`None`, :func:`thesis.manuscripts` is used.
    root
        The directory which holds the downloaded manuscripts.
        If :obj:`None`, :obj:`thesis.directory_manuscripts` is used.
    directory
        The directory to build the thesis in.
        If :obj:`None`, :obj:`directory_build` is used.
    """
    if manuscripts is None:
        manuscripts = thesis.manuscripts()
    if root is None:
        root = thesis.directory_manuscripts
    if directory is None:
        directory = directory_build

    doc = document(manuscripts=manuscripts, root=root)

    (directory / "manuscripts").mkdir(parents=True, exist_ok=True)
    bibliographies = [pathlib.Path(__file__).parent / "sources.bib"]
    for manuscript in manuscripts:
        shutil.copy2(
            src=manuscript.pdf(root),
            dst=directory / "manuscripts" / f"{manuscript.name}.pdf",
        )
        bibliographies.append(manuscript.bib(root))

    references = thesis.bibliography(bibliographies)
    (directory / "references.bib").write_text(references, encoding="utf-8")

    path = directory / "thesis"
    doc.generate_pdf(
        filepath=path,
        clean_tex=False,
    )

    return path.with_suffix(".pdf")
