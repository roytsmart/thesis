import dataclasses
import os
import pathlib
import shutil
import subprocess
import sys
from typing import Literal

__all__ = [
    "Author",
    "Manuscript",
    "directory_manuscripts",
    "manuscripts",
]

directory_manuscripts = pathlib.Path(__file__).parent / "manuscripts"
"""
Where :meth:`Manuscript.build` puts the manuscripts by default, and where
:func:`thesis.pdf` looks for them.
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
    builds, with the line numbers for review turned off.
    The article is built in an environment of its own, since the articles do
    not all depend on the same versions of the same packages.
    """

    name: str
    """A short name for the manuscript, used for its directory and labels."""

    title: str
    """The title of the manuscript, which is also the title of the chapter."""

    authors: list[Author]
    """The authors of the manuscript, in the order they appear on it."""

    module: str
    """
    The name of the Python package which builds the manuscript, whose
    ``pdf(linenumbers)`` function returns the path of the PDF it built.
    """

    stem: str
    """The name of the PDF the package builds, without its extension."""

    repository: str
    """The URL of the repository of the manuscript."""

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
        The directory the built manuscript is kept in.

        Parameters
        ----------
        root
            The directory which holds the directories of every manuscript.
        """
        return root / self.name

    def pdf(self, root: pathlib.Path = directory_manuscripts) -> pathlib.Path:
        """
        The PDF of the built manuscript.

        Parameters
        ----------
        root
            The directory which holds the directories of every manuscript.
        """
        return self.directory(root) / f"{self.stem}.pdf"

    def build(
        self,
        python: str | os.PathLike = sys.executable,
        root: pathlib.Path = directory_manuscripts,
    ) -> pathlib.Path:
        """
        Build the PDF of the manuscript without line numbers, and copy it,
        its formatted bibliography, and its BibTeX files into
        :meth:`directory`.

        Parameters
        ----------
        python
            The Python interpreter of an environment which has the package
            of the manuscript installed.
        root
            The directory which holds the directories of every manuscript.
        """
        directory = self.directory(root)
        directory.mkdir(parents=True, exist_ok=True)

        code = f"import {self.module}; print({self.module}.pdf(linenumbers=False))"
        process = subprocess.run(
            [os.fspath(python), "-c", code],
            capture_output=True,
            text=True,
            check=False,
            # Run outside of any source tree, so that the package is imported
            # from where it is installed.
            cwd=directory,
            env=os.environ | {"MPLBACKEND": "agg"},
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"building {self.module} failed:\n{process.stderr[-4000:]}"
            )

        source = pathlib.Path(process.stdout.strip().splitlines()[-1])
        paths = [source, source.with_suffix(".bbl"), *source.parent.glob("*.bib")]
        for path in paths:
            shutil.copy2(path, directory / path.name)

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
            module="esis_instrument_paper",
            stem="esis-instrument",
            repository="https://github.com/esis-mission/esis-instrument-paper",
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
            module="ccd_snr",
            stem="ccd-euv-snr",
            repository="https://github.com/roytsmart/ccd-noise-paper",
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
            module="ccd_diffusion",
            stem="ccd-diffusion",
            repository="https://github.com/roytsmart/ccd-diffusion-paper",
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
            module="esis_jet_paper",
            stem="esis-jet",
            repository="https://github.com/esis-mission/esis-jet-paper",
        ),
    ]
