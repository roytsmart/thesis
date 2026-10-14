import pathlib

import thesis


def test_headings(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    expected = [
        thesis.Heading(level=1, title="Abstract", page=1),
        thesis.Heading(level=1, title="Introduction", page=1),
        thesis.Heading(level=2, title="The Details", page=2),
        thesis.Heading(level=3, title="The Finer Details", page=2),
        thesis.Heading(level=1, title="An Appendix", page=3),
        thesis.Heading(level=1, title="References", page=3),
    ]
    for manuscript in manuscripts:
        assert thesis.headings(manuscript.pdf(root)) == expected


def test_headings_depth(
    manuscripts: list[thesis.Manuscript],
    root: pathlib.Path,
) -> None:
    manuscript = manuscripts[0]
    result = thesis.headings(manuscript.pdf(root), depth=1)
    assert all(heading.level == 1 for heading in result)
