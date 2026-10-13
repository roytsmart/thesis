import pathlib
import sys
import textwrap

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


def test_build(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package = tmp_path / "packages" / "article"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text(
        textwrap.dedent('''
            import pathlib

            def pdf(linenumbers: bool = True) -> pathlib.Path:
                """A stand-in for the package of an article."""
                directory = pathlib.Path(__file__).parent
                path = directory / "article.pdf"
                path.write_text(f"linenumbers={linenumbers}")
                path.with_suffix(".bbl").write_text("bbl")
                (directory / "sources.bib").write_text("bib")
                return path
        '''),
        encoding="utf-8",
    )
    monkeypatch.setenv("PYTHONPATH", str(package.parent))

    manuscript = thesis.Manuscript(
        name="article",
        title="An Article",
        authors=[thesis.Author("Roy T. Smart")],
        module="article",
        stem="article",
        repository="https://github.com/roytsmart/article",
        layout=thesis.aastex_twocolumn,
    )

    root = tmp_path / "manuscripts"
    result = manuscript.build(python=sys.executable, root=root)

    # The article is built as its repository builds it, so its draft keeps
    # its line numbers.
    assert result == root / "article" / "article.pdf"
    assert result.read_text() == "linenumbers=True"
    assert result.with_suffix(".bbl").exists()
    assert (result.parent / "sources.bib").exists()


def test_build_failure(tmp_path: pathlib.Path) -> None:
    manuscript = thesis.Manuscript(
        name="missing",
        title="A Missing Article",
        authors=[thesis.Author("Roy T. Smart")],
        module="a_package_which_does_not_exist",
        stem="missing",
        repository="https://github.com/roytsmart/missing",
        layout=thesis.aastex_twocolumn,
    )
    with pytest.raises(RuntimeError, match="a_package_which_does_not_exist"):
        manuscript.build(python=sys.executable, root=tmp_path)
