import pylatex

__all__ = [
    "abstract",
    "front",
]


def front() -> list[pylatex.NoEscape]:
    """
    The information on the title and copyright pages, and in the properties
    of the PDF.

    The Graduate School asks for the fullest form of the name of the author
    (first, middle, and last) on the title and copyright pages, and for the
    title, author, and language to be set in the properties of the PDF.
    """
    name = "Roy Thomas Smart"
    title = "Computed Tomography Imaging Spectroscopy of the Solar Transition Region"
    return [
        pylatex.NoEscape(rf"\name{{{name}}}"),
        pylatex.NoEscape(rf"\DocTitle{{{title}}}"),
        pylatex.NoEscape(r"\degreetitle{Physics}"),
        pylatex.NoEscape(r"\department{Physics}"),
        pylatex.NoEscape(r"\committeechair{Charles C. Kankelborg}"),
        pylatex.NoEscape(r"\graduationdate{May 2027}"),
        pylatex.NoEscape(r"\copyrightyear{2027}"),
        pylatex.NoEscape(rf"\hypersetup{{pdftitle={{{title}}}, pdfauthor={{{name}}}}}"),
    ]


def abstract() -> pylatex.NoEscape:
    """
    The abstract of the thesis, which the Graduate School asks to be no more
    than 350 words, without formulas or abbreviations, and understandable by
    a reader who is not an expert in the field.
    """
    return pylatex.NoEscape(r"""
\begin{abstract}
\begin{outline}
\item A statement of the problem.
\item The procedure or methods.
\item The results.
\item The conclusions.
\end{outline}
\end{abstract}""")
