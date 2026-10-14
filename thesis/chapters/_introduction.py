from ._chapter import Chapter

__all__ = [
    "introduction",
]


def introduction() -> Chapter:
    """
    The general introduction, which the Graduate School requires and which
    must be solely the student's own writing.
    """
    result = Chapter("Introduction")
    result.append(r"""
\begin{outline}
\item The problem context for the manuscripts.
\item The purpose and objectives of the work.
\item How each manuscript addresses the purpose and objectives, linking the
    manuscripts thematically.
\end{outline}""")
    return result
