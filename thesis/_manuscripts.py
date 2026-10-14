import dataclasses
import pathlib
import urllib.request
from typing import Literal

from ._layout import Layout, aastex_twocolumn, spieman

__all__ = [
    "Author",
    "Manuscript",
    "directory_manuscripts",
    "manuscripts",
]

directory_manuscripts = pathlib.Path(__file__).parent / "manuscripts"
"""
Where :meth:`Manuscript.download` puts the manuscripts by default, and
where :func:`thesis.pdf` looks for them.
"""


@dataclasses.dataclass
class Author:
    """
    An author of a manuscript, as listed on its Contribution of Authors and
    Co-Authors page.
    """

    name: str
    """The name of the author, as it appears on the manuscript."""

    contributions: None | str = None
    """
    A brief paragraph of what this author contributed to the manuscript, or
    :obj:`None` if it has not been written yet.
    """


@dataclasses.dataclass
class Manuscript:
    """
    A journal article included as a chapter of the thesis.

    The Graduate School allows the chapter to keep the formatting of the
    journal, so the article is inserted as the PDF that its own repository
    builds, as it is.
    The pages are scaled to fit the :class:`Layout` of the class of the
    journal into the text block of the thesis, so a draft is scaled as its
    final version will be, and its line numbers stay in the margin.
    The article is downloaded from where its repository publishes it, with
    its formatted bibliography and its BibTeX file, rather than built here,
    since the articles do not all depend on the same versions of the same
    packages.
    """

    name: str
    """A short name for the manuscript, used for its directory and labels."""

    title: str
    """The title of the manuscript, which is also the title of the chapter."""

    authors: list[Author]
    """The authors of the manuscript, in the order they appear on it."""

    stem: str
    """
    The name the repository publishes the PDF, the formatted bibliography,
    and the BibTeX file of the manuscript under, without their extensions.
    """

    repository: str
    """The URL of the repository of the manuscript."""

    url: str
    """
    The URL of the directory the repository publishes the manuscript to, on
    GitHub Pages.
    """

    layout: Layout
    """
    Where the class of the journal prints on the page, which is scaled to
    fit the text block of the thesis.
    """

    status: Literal["prepared", "submitted", "accepted", "published"] = "prepared"
    """
    How far the manuscript is through peer review: prepared for submission,
    officially submitted, accepted, or published.
    """

    journal: None | str = None
    """The journal the manuscript was accepted by or published in."""

    publisher: None | str = None
    """The publisher of the journal, if the manuscript was accepted."""

    submitted: None | str = None
    """The date the manuscript was submitted."""

    appears: None | str = None
    """The date the manuscript will appear, if it was accepted."""

    issue: None | str = None
    """The issue the manuscript appears in, if it was published."""

    doi: None | str = None
    """The DOI of the manuscript, if it has one."""

    def directory(self, root: pathlib.Path = directory_manuscripts) -> pathlib.Path:
        """
        The directory the downloaded manuscript is kept in.

        Parameters
        ----------
        root
            The directory which holds the directories of every manuscript.
        """
        return root / self.name

    def pdf(self, root: pathlib.Path = directory_manuscripts) -> pathlib.Path:
        """
        The PDF of the downloaded manuscript.

        Parameters
        ----------
        root
            The directory which holds the directories of every manuscript.
        """
        return self.directory(root) / f"{self.stem}.pdf"

    def bbl(self, root: pathlib.Path = directory_manuscripts) -> pathlib.Path:
        """
        The formatted bibliography of the downloaded manuscript, which lists
        what it cites.

        Parameters
        ----------
        root
            The directory which holds the directories of every manuscript.
        """
        return self.directory(root) / f"{self.stem}.bbl"

    def bib(self, root: pathlib.Path = directory_manuscripts) -> pathlib.Path:
        """
        The BibTeX file the bibliography of the downloaded manuscript was
        formatted from.

        Parameters
        ----------
        root
            The directory which holds the directories of every manuscript.
        """
        return self.directory(root) / f"{self.stem}.bib"

    def download(
        self,
        url: None | str = None,
        root: pathlib.Path = directory_manuscripts,
    ) -> pathlib.Path:
        """
        Download the PDF of the manuscript, its formatted bibliography, and
        its BibTeX file into :meth:`directory`, and return the path of the
        PDF.

        Nothing is written unless all three are downloaded, so that the PDF
        of one build is never paired with the bibliography of another.

        Parameters
        ----------
        url
            The URL of the directory to download the manuscript from, such
            as the preview of a pull request to the repository of the
            manuscript.
            If :obj:`None`, :attr:`url` is used.
        root
            The directory which holds the directories of every manuscript.
        """
        if url is None:
            url = self.url

        paths = [self.pdf(root), self.bbl(root), self.bib(root)]

        contents = []
        for path in paths:
            with urllib.request.urlopen(
                f"{url.rstrip('/')}/{path.name}",
                timeout=60,
            ) as response:
                contents.append(response.read())

        self.directory(root).mkdir(parents=True, exist_ok=True)
        for path, content in zip(paths, contents, strict=True):
            path.write_bytes(content)

        return self.pdf(root)


def manuscripts() -> list[Manuscript]:
    """
    The manuscripts included in the thesis, in the order of their chapters.
    """
    return [
        Manuscript(
            name="instrument",
            title="The EUV Snapshot Imaging Spectrograph",
            authors=[
                Author("Roy T. Smart"),
                Author("Hans T. Courrier"),
                Author("Jacob D. Parker"),
                Author("Charles C. Kankelborg"),
                Author("Amy R. Winebarger"),
                Author("Ken Kobayashi"),
                Author("Brent Beabout"),
                Author("Dyana Beabout"),
                Author("Ben Carrol"),
                Author("Jonathan Cirtain"),
                Author("James A. Duffy"),
                Author("Eric Gullikson"),
                Author("Micah Johnson"),
                Author("Laurel Rachmeler"),
                Author("Larry Springer"),
                Author("David L. Windt"),
            ],
            stem="esis-instrument",
            repository="https://github.com/esis-mission/esis-instrument-paper",
            url="https://esis-mission.github.io/esis-instrument-paper/",
            layout=aastex_twocolumn,
        ),
        Manuscript(
            name="noise",
            title=(
                "The Noise on Ultraviolet Astronomical Images Captured by "
                "Back-illuminated Silicon Sensors"
            ),
            authors=[
                Author("Roy T. Smart"),
                Author("Charles C. Kankelborg"),
                Author("Jacob D. Parker"),
            ],
            stem="ccd-euv-snr",
            repository="https://github.com/roytsmart/ccd-noise-paper",
            url="https://roytsmart.github.io/ccd-noise-paper/",
            layout=aastex_twocolumn,
        ),
        Manuscript(
            name="diffusion",
            title=(
                "Measuring the Charge-diffusion Kernel of a Back-illuminated "
                "CCD in Orbit from Glancing Particle Tracks"
            ),
            authors=[
                Author("Roy T. Smart"),
                Author("Charles C. Kankelborg"),
            ],
            stem="ccd-diffusion",
            repository="https://github.com/roytsmart/ccd-diffusion-paper",
            url="https://roytsmart.github.io/ccd-diffusion-paper/",
            layout=spieman,
        ),
        Manuscript(
            name="jet",
            title=(
                "Flows, Magnetic Topology, and Temperature of a Transition "
                "Region Jet Observed by the EUV Snapshot Imaging Spectrograph"
            ),
            authors=[
                Author("Roy T. Smart"),
                Author("Charles C. Kankelborg"),
                Author("Jacob D. Parker"),
                Author("Dana W. Longcope"),
            ],
            stem="esis-jet",
            repository="https://github.com/esis-mission/esis-jet-paper",
            url="https://esis-mission.github.io/esis-jet-paper/",
            layout=aastex_twocolumn,
        ),
    ]
