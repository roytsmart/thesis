import collections.abc
import pathlib
import re
import warnings

__all__ = [
    "bibliography",
    "citations",
]


def citations(path: pathlib.Path) -> list[str]:
    """
    The keys of every entry in a bibliography formatted by BibTeX, in the
    order they appear.

    The Graduate School asks for a cumulative list of references at the end
    of the thesis, covering every reference cited in each manuscript, so
    these are the keys the thesis has to cite to reproduce the references of
    a manuscript.

    Parameters
    ----------
    path
        The ``.bbl`` file written by BibTeX for the manuscript.
    """
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")

    result = []
    for match in re.finditer(r"\\bibitem\s*", text):
        index = match.end()
        if text.startswith("[", index):
            depth = 0
            while index < len(text):
                character = text[index]
                if character == "{":
                    depth += 1
                elif character == "}":
                    depth -= 1
                elif character == "]" and depth == 0:
                    break
                index += 1
            index += 1
        key = re.match(r"\s*\{([^}]*)\}", text[index:])
        if key is not None:
            result.append(key.group(1).strip())

    return result


def _entries(text: str) -> list[tuple[None | str, str]]:
    """
    Split the text of a BibTeX file into its entries.

    Parameters
    ----------
    text
        The contents of the BibTeX file.

    Returns
    -------
        The key and text of each entry, where the key is :obj:`None` for the
        ``@string`` and ``@preamble`` commands, which have none.
    """
    starts = [m.start() for m in re.finditer(r"^\s*@", text, flags=re.MULTILINE)]
    result = []
    for start, stop in zip(starts, starts[1:] + [len(text)]):
        entry = text[start:stop].strip()
        kind = re.match(r"@\s*(\w+)", entry)
        if kind is None:
            continue
        kind = kind.group(1).casefold()
        if kind == "comment":
            continue
        if kind in ("string", "preamble"):
            result.append((None, entry))
            continue
        key = re.match(r"@\s*\w+\s*[{(]\s*([^,\s]+)\s*,", entry)
        if key is None:
            continue
        result.append((key.group(1), entry))
    return result


def bibliography(paths: collections.abc.Sequence[pathlib.Path]) -> str:
    """
    Merge several BibTeX files into one, keeping the first entry with each
    key.

    The manuscripts often cite the same work under the same key, and BibTeX
    complains about an entry it has seen before, so each key is kept once.
    BibTeX does not distinguish keys by case, so neither does this.
    Two entries with the same key but a different title are probably two
    different works, which would leave one of the manuscripts citing the
    wrong one, so this warns about them.

    Parameters
    ----------
    paths
        The BibTeX files, in order of precedence.
    """
    seen: dict[str, str] = {}
    commands = []
    result = []

    for path in paths:
        text = pathlib.Path(path).read_text(encoding="utf-8")
        for key, entry in _entries(text):
            if key is None:
                if entry not in commands:
                    commands.append(entry)
                continue
            if key.casefold() in seen:
                if _title(seen[key.casefold()]) != _title(entry):
                    warnings.warn(
                        f"the BibTeX entry {key!r} in {path} has a different "
                        f"title than the entry with the same key before it, "
                        f"which is kept."
                    )
                continue
            seen[key.casefold()] = entry
            result.append(entry)

    return "\n\n".join(commands + result) + "\n"


def _title(entry: str) -> str:
    """
    The title of a BibTeX entry, with everything but its letters and digits
    removed, so that two copies of an entry exported with different
    formatting have the same title.

    Parameters
    ----------
    entry
        The text of the entry.
    """
    match = re.search(
        r"^\s*title\s*=\s*(.*?)(?=,\s*\n\s*\w+\s*=|,?\s*\}\s*\Z)",
        entry,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if match is None:
        return ""
    return re.sub(r"\W+", "", match.group(1)).casefold()
