import importlib.resources
import re

import pylatex

__all__ = [
    "preamble",
]


def _journals() -> list[pylatex.NoEscape]:
    """
    The abbreviations of journal names which the AAS bibliographies use.

    The manuscripts cite entries exported from ADS, whose journal names are
    macros like ``\\apj`` that the AASTeX class defines.
    The thesis is not built with that class, so the same macros are defined
    here from the copy of it which :mod:`aastex` ships.
    """
    path = importlib.resources.files("aastex") / "aastex701.cls"
    text = path.read_bytes().decode("utf-8", errors="replace")
    result = [
        pylatex.NoEscape(rf"\providecommand{{\{name}}}{{{value}}}")
        for name, value in re.findall(
            r"\\newcommand\\(\w+)\{\\ref@jnl\{([^{}]*)\}\}", text
        )
    ]
    result.append(
        pylatex.NoEscape(r"\providecommand{\ptrlond}{Phil.~Trans.~R.~Soc.~London}")
    )
    result.append(pylatex.NoEscape(r"\providecommand{\bibinfo}[2]{#2}"))
    return result


def preamble() -> list[pylatex.Package | pylatex.NoEscape]:
    """
    Custom LaTeX commands used throughout the thesis.
    """
    return [
        pylatex.Package("amssymb"),
        pylatex.Package("natbib"),
        pylatex.Package("pdfpages"),
        pylatex.Package("xcolor"),
        # Each manuscript is inserted as the PDF its repository builds, which
        # the Graduate School allows as long as the page numbers of the thesis
        # continue through it and it stays inside the margins.
        # So the pages are trimmed to their ink, scaled to fit the text block,
        # centered on it, and given the page style of the thesis, which puts
        # the page number in the header.
        # The offset is expanded to plain lengths first, since pdfpages does
        # not evaluate expressions in its options.
        pylatex.NoEscape(r"""
\makeatletter
\newcommand{\includemanuscript}[2][]{%
  \edef\manuscript@offset{%
    \the\dimexpr 1in + \hoffset + \oddsidemargin + 0.5\textwidth - 0.5\paperwidth\relax
    \space
    \the\dimexpr 0.5\paperheight - 1in - \voffset - \topmargin - \headheight - \headsep - 0.5\textheight\relax
  }%
  \edef\manuscript@include{%
    \noexpand\includepdf[
      pages=-,
      clip,
      width=\noexpand\textwidth,
      height=\noexpand\textheight,
      keepaspectratio,
      offset=\manuscript@offset,
      pagecommand={\noexpand\thispagestyle{plain}},
      \unexpanded{#1}
    ]{\unexpanded{#2}}%
  }%
  \manuscript@include
}
\makeatother"""),
        # The parts of the thesis which are not written yet are drafted as a
        # list of what each will contain, set apart from the prose so that a
        # reader of the draft can tell the plan from the thesis.
        pylatex.NoEscape(r"""
\newenvironment{outline}
  {\par\color{gray}\noindent\textbf{Outline.}\begin{itemize}}
  {\end{itemize}}"""),
        *_journals(),
    ]
