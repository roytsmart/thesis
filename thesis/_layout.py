import dataclasses

__all__ = [
    "Layout",
    "aastex_twocolumn",
    "spieman",
]


@dataclasses.dataclass(frozen=True)
class Layout:
    """
    The region of the page which the class of a journal prints on: the
    running heads, the text, and the page numbers, but not the line numbers
    of a draft, which are in the margin outside of it.

    The pages of a manuscript are scaled to fit this region into the text
    block of the thesis, so the scale is set by the class rather than by
    what is on the pages.
    A draft with its lines numbered, or an equation which runs into the
    margin, is scaled the same as the final version, and whatever is outside
    of this region stays in the margin of the thesis.

    Positions are in big points from the top left corner of the page.
    """

    left: float
    """The left edge of the region."""

    top: float
    """The top edge of the region."""

    right: float
    """The right edge of the region."""

    bottom: float
    """The bottom edge of the region."""

    width: float = 612
    """The width of the page, which is letter paper unless given."""

    height: float = 792
    """The height of the page, which is letter paper unless given."""

    @property
    def trim(self) -> tuple[float, float, float, float]:
        """
        How much of the left, bottom, right, and top of the page is outside
        of the region, in the order that the ``trim`` option of
        ``\\includegraphics`` expects.
        """
        return (
            self.left,
            self.height - self.bottom,
            self.width - self.right,
            self.top,
        )


aastex_twocolumn = Layout(
    left=72 - 7.5 / 25.4 * 72,
    top=37,
    right=72 - 7.5 / 25.4 * 72 + 7.1 * 72,
    bottom=720,
)
"""
The layout of AASTeX 7 in its ``twocolumn`` style.

The text is 7.1 inches wide, and is shifted 7.5 millimeters to the left of
the usual margin of an inch (``\\textwidth`` and ``\\hoffset``).
It ends 717 big points down the page, and the descenders of its last line
reach 720.
Above it is the running head of each page, 45 big points down, and on the
first page the "Draft version" line, 37 big points down.
"""

spieman = Layout(
    left=72,
    top=72,
    right=72 + 6.5 * 72,
    bottom=751,
)
"""
The layout of ``spieman``, the class of the SPIE journals, at 12 points.

The text is 6.5 by 9 inches, inside margins of an inch, and the page number
is centered 30 points below it, its bottom 751 big points down the page.
"""
