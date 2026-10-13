import pytest

import thesis


def test_trim() -> None:
    layout = thesis.Layout(left=50, top=40, right=562, bottom=752)
    assert layout.trim == (50, 792 - 752, 612 - 562, 40)


@pytest.mark.parametrize(
    argnames="layout,width",
    argvalues=[
        (thesis.aastex_twocolumn, 7.1 * 72),
        (thesis.spieman, 6.5 * 72),
    ],
)
def test_layouts(layout: thesis.Layout, width: float) -> None:
    assert layout.right - layout.left == pytest.approx(width)
    assert 0 < layout.left < layout.right < layout.width
    assert 0 < layout.top < layout.bottom < layout.height
