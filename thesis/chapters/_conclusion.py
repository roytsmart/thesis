from ._chapter import Chapter

__all__ = [
    "conclusion",
]


def conclusion() -> Chapter:
    """
    The general conclusion, which the Graduate School requires and which must
    be solely the student's own writing.
    """
    result = Chapter("Conclusion")
    result.append(r"""
\begin{outline}
\item Link the manuscripts thematically.
\item Future directions of research.
\end{outline}""")
    return result
