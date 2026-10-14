import dataclasses
import pathlib
import shutil
import urllib.error

import pytest

import thesis


def test_manuscripts() -> None:
    manuscripts = thesis.manuscripts()

    # The Graduate School asks a doctoral thesis in the Scholarly Works
    # Option for at least two manuscripts, at least one of them first-authored
    # by the student.
    assert len(manuscripts) >= 2
    assert any(m.authors[0].name == "Roy T. Smart" for m in manuscripts)

    names = [m.name for m in manuscripts]
    assert len(set(names)) == len(names)

    for manuscript in manuscripts:
        assert manuscript.status in ("prepared", "submitted", "accepted", "published")

    # Each author has contributions of their own to each manuscript.
    authors = [id(author) for m in manuscripts for author in m.authors]
    assert len(set(authors)) == len(authors)


def _files(
    manuscript: thesis.Manuscript,
    root: pathlib.Path,
) -> list[pathlib.Path]:
    """
    The PDF, the formatted bibliography, and the BibTeX file of a manuscript.

    Parameters
    ----------
    manuscript
        The manuscript.
    root
        The directory which holds the directories of every manuscript.
    """
    return [manuscript.pdf(root), manuscript.bbl(root), manuscript.bib(root)]


def test_download(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    # The manuscript written by the fixture stands in for one published by
    # its repository.
    published = manuscripts[0]
    manuscript = dataclasses.replace(
        published,
        url=published.directory(root).as_uri(),
    )

    destination = tmp_path / "downloaded"
    result = manuscript.download(root=destination)

    assert result == manuscript.pdf(destination)
    for a, b in zip(_files(published, root), _files(manuscript, destination)):
        assert a.read_bytes() == b.read_bytes()


def test_download_url(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    # A manuscript can be downloaded from somewhere other than where its
    # repository publishes it, like the preview of a pull request.
    published = manuscripts[0]
    manuscript = dataclasses.replace(
        published,
        url=(tmp_path / "nowhere").as_uri(),
    )

    destination = tmp_path / "downloaded"
    manuscript.download(url=published.directory(root).as_uri(), root=destination)

    for a, b in zip(_files(published, root), _files(manuscript, destination)):
        assert a.read_bytes() == b.read_bytes()


def test_download_incomplete(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    # A repository which publishes the PDF without its BibTeX file.
    manuscript = manuscripts[0]
    incomplete = tmp_path / "incomplete"
    incomplete.mkdir()
    shutil.copy2(manuscript.pdf(root), incomplete)
    shutil.copy2(manuscript.bbl(root), incomplete)

    destination = tmp_path / "downloaded"
    with pytest.raises(urllib.error.URLError):
        manuscript.download(url=incomplete.as_uri(), root=destination)

    # Nothing is written, so a PDF is never left beside the bibliography of
    # another build.
    assert not manuscript.directory(destination).exists()
