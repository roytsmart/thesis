from ._chapter import Chapter

__all__ = [
    "methodology",
]


def methodology() -> Chapter:
    """
    The methodology, which the Graduate School highly recommends but does not
    require.
    """
    result = Chapter("Methodology")
    result.append(r"""
\begin{outline}
\item More detail on the methods than the manuscripts had room for.
\end{outline}""")
    return result
