import pylatex

__all__ = [
    "Chapter",
]


class Chapter(pylatex.Chapter):
    """
    A chapter of the thesis, whose contents are written in LaTeX.
    """

    def __init__(
        self,
        title: str,
        *,
        label: pylatex.Label | bool | str = True,
    ) -> None:
        """
        Parameters
        ----------
        title
            The title of the chapter.
        label
            The label of the chapter, as for :class:`pylatex.Section`.
        """
        super().__init__(title=pylatex.NoEscape(title), label=label)
        self.escape = False
