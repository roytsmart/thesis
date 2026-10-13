import pathlib

import pymupdf
import pytest

import thesis


def test_trim(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    manuscript = manuscripts[0]
    result = thesis.trim(manuscript.pdf(root))
    expected = (50 - 1, 792 - 752 - 1, 612 - 562 - 1, 40 - 1)
    assert result == pytest.approx(expected, abs=1)


def test_trim_blank(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "blank.pdf"
    document = pymupdf.open()
    document.new_page(width=612, height=792)
    document.save(path)
    document.close()
    with pytest.raises(ValueError, match="blank"):
        thesis.trim(path)


def test_headings(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    manuscript = manuscripts[0]
    result = thesis.headings(manuscript.pdf(root))
    assert result == [
        thesis.Heading(level=1, title="Abstract", page=1),
        thesis.Heading(level=1, title="Introduction", page=1),
        thesis.Heading(level=2, title="The Details", page=2),
        thesis.Heading(level=3, title="The Finer Details", page=2),
        thesis.Heading(level=1, title="An Appendix", page=3),
        thesis.Heading(level=1, title="References", page=3),
    ]


def test_headings_depth(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    manuscript = manuscripts[0]
    result = thesis.headings(manuscript.pdf(root), depth=1)
    assert all(heading.level == 1 for heading in result)
