# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`thesis` is a **reproducible doctoral dissertation**, not a conventional
software library. The `thesis` Python package generates the LaTeX of a
Montana State University dissertation in the Graduate School's Scholarly
Works Option and compiles it with `thesis.pdf()`.

This is one package within the larger Kankelborg-Group workspace (see the
parent `../CLAUDE.md`). Four of its chapters are journal articles from sibling
repositories, `esis-instrument-paper`, `ccd-noise-paper` (checked out locally
as `ccd-snr-paper`), `ccd-diffusion-paper`, and `esis-jet-paper`, which are
inserted as the PDFs those repositories build.

## Rules

- **The rules of the Graduate School are the specification.** They are at
  https://www.montana.edu/etd/formatting/scholarly-works-option.html, with
  sample pages linked from there. Check a change against them, not only
  against the tests.
- **The introduction, methodology, conclusion, and abstract are the
  student's own writing.** The Graduate School requires the introduction and
  conclusion to be solely the student's work, so never draft their prose.
  Leave them as an `outline` of what each must contain.
- **Never reformat the manuscripts.** They are inserted as the PDFs their
  repositories build, line numbers and all. A change to an article belongs in
  the repository of the article.
- **The scale comes from the `Layout` of the journal's class, never from the
  ink on the pages**, so that a draft is scaled as its final version will
  be, and an equation which runs into the margin cannot shrink a whole
  article.
- **Do not import the packages of the articles.** They pin incompatible
  versions of `optika` and `aastex`, so each is built in its own environment
  by `Manuscript.build()`, which runs it in a subprocess.
- `thesis/MSUstyle.cls` is vendored from the Graduate School's template and
  is licensed CC BY-NC-SA 3.0; do not edit it.

## Commands

Run from the repository root:

```bash
pip install -e .[test]          # install for development
pytest                          # run tests; test_pdf compiles a small thesis
black thesis                    # format (CI enforces --check)
ruff check                      # lint (CI enforces)
```

## Architecture

- **`_document.py`**: `document()` builds the thesis on `MSUstyle`, and
  `pdf()` copies the manuscripts into `thesis/build/`, merges their
  bibliographies into `references.bib` there, and compiles it.
- **`_manuscripts.py`**: `Manuscript` describes an article (its authors and
  their contributions, its status in peer review, the package which builds
  it), and `manuscripts()` lists them in the order of their chapters.
- **`_layout.py`**: `Layout` is the region of the page a journal's class
  prints on, which is scaled into the text block of the thesis, with the
  layouts of AASTeX (`aastex_twocolumn`) and SPIE (`spieman`).
- **`_pages.py`**: `headings()` reads the bookmarks of a PDF, checked against
  the text of its pages.
- **`_references.py`**: `citations()` reads the keys of a `.bbl` file, and
  `bibliography()` merges BibTeX files.
- **`_preamble.py`**: `\includemanuscript`, which inserts a manuscript into
  the text block with the page numbers of the thesis, and the journal
  macros of AASTeX which the bibliographies use.
- **`chapters/`**: each module returns a `Chapter`.

## Conventions

- Every module declares an explicit `__all__` and exposes functionality through small
  factory functions, re-exported up the package via `__init__.py`.
- Modules import the top-level package as `import thesis` and reach back into it
  at call time.
- Generated LaTeX/PDF output and the built manuscripts are gitignored; never commit them.
- Stage explicit files with `git add`; never `git add` whole directories.
