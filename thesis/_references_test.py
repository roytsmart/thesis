import pathlib
import warnings

import pytest

import thesis


@pytest.mark.parametrize(
    argnames="text,expected",
    argvalues=[
        (
            (
                "\\begin{thebibliography}{}\n"
                "\\bibitem[{P. {Astier} {et~al.}(2019){Astier}, {Le\n"
                "  Breton}, \\& {Sepulveda}}]{Astier2019}\n"
                "{Astier}, P. 2019, \\aap, 629, A36\n"
                "\\bibitem[{{Fano}(1947)}]{Fano1947}\n"
                "{Fano}, U. 1947\n"
                "\\end{thebibliography}\n"
            ),
            ["Astier2019", "Fano1947"],
        ),
        (
            (
                "\\begin{thebibliography}{1}\n"
                "\\bibitem{Janesick2001}\n"
                "J. R. Janesick, Scientific Charge-Coupled Devices (2001).\n"
                "\\bibitem{Stern1994} R. A. Stern et al., Appl. Opt. (1994).\n"
                "\\end{thebibliography}\n"
            ),
            ["Janesick2001", "Stern1994"],
        ),
    ],
)
def test_citations(tmp_path: pathlib.Path, text: str, expected: list[str]) -> None:
    path = tmp_path / "article.bbl"
    path.write_text(text, encoding="utf-8")
    assert thesis.citations(path) == expected


def test_bibliography(tmp_path: pathlib.Path) -> None:
    first = tmp_path / "first.bib"
    first.write_text(
        "@string{apj = {ApJ}}\n"
        "@comment{ignored}\n"
        "@article{Doe2020,\n  title = {A Work},\n}\n"
        "@article{Roe2021,\n  title = {Another Work},\n}\n",
        encoding="utf-8",
    )
    second = tmp_path / "second.bib"
    second.write_text(
        "@string{apj = {ApJ}}\n"
        "@article{Doe2020,\n    title = {A Work},\n}\n"
        '@ARTICLE{roe2021,\n  title = "{Another work}",\n  year = 2021\n}\n'
        "@book{Poe2022,\n  title = {A Book},\n}\n",
        encoding="utf-8",
    )

    # Copies of the same work, whose keys differ only in case or whose
    # entries are formatted differently, are not a conflict.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = thesis.bibliography([first, second])

    assert result.count("@string") == 1
    assert "@comment" not in result
    assert result.count("Doe2020") == 1
    assert "Roe2021" in result
    assert "roe2021" not in result
    assert "Poe2022" in result


def test_bibliography_conflict(tmp_path: pathlib.Path) -> None:
    first = tmp_path / "first.bib"
    first.write_text("@article{Doe2020,\n  title = {A Work},\n}\n", encoding="utf-8")
    second = tmp_path / "second.bib"
    second.write_text("@article{Doe2020,\n  title = {Another},\n}\n", encoding="utf-8")

    with pytest.warns(UserWarning, match="Doe2020"):
        result = thesis.bibliography([first, second])

    assert "A Work" in result
    assert "Another" not in result
