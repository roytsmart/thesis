# thesis

[![tests](https://github.com/roytsmart/thesis/actions/workflows/tests.yml/badge.svg)](https://github.com/roytsmart/thesis/actions/workflows/tests.yml)
[![Black](https://github.com/roytsmart/thesis/actions/workflows/black.yml/badge.svg)](https://github.com/roytsmart/thesis/actions/workflows/black.yml)
[![Ruff](https://github.com/roytsmart/thesis/actions/workflows/ruff.yml/badge.svg)](https://github.com/roytsmart/thesis/actions/workflows/ruff.yml)

The doctoral dissertation of Roy T. Smart, Department of Physics, Montana State
University.

The dissertation follows the Graduate School's
[Scholarly Works Option](https://www.montana.edu/etd/formatting/scholarly-works-option.html),
in which each of its chapters about a manuscript keeps the formatting of the
journal. The manuscripts are:

| Chapter | Manuscript | Repository |
|---|---|---|
| 3 | The EUV Snapshot Imaging Spectrograph | [esis-mission/esis-instrument-paper](https://github.com/esis-mission/esis-instrument-paper) |
| 4 | The Noise on Ultraviolet Astronomical Images Captured by Back-illuminated Silicon Sensors | [roytsmart/ccd-noise-paper](https://github.com/roytsmart/ccd-noise-paper) |
| 5 | Measuring the Charge-diffusion Kernel of a Back-illuminated CCD in Orbit from Glancing Particle Tracks | [roytsmart/ccd-diffusion-paper](https://github.com/roytsmart/ccd-diffusion-paper) |
| 6 | Flows, Magnetic Topology, and Temperature of a Transition Region Jet Observed by the EUV Snapshot Imaging Spectrograph | [esis-mission/esis-jet-paper](https://github.com/esis-mission/esis-jet-paper) |

They are surrounded by the chapters the Graduate School requires of the
student alone: a general introduction, a methodology, and a general
conclusion.

## How the thesis is assembled

The `thesis` Python package generates the LaTeX of the thesis on the
Graduate School's class, `MSUstyle.cls`, and compiles it.

- **The manuscripts are inserted as PDFs**, as each repository above builds
  them, and given the page numbers of the thesis in the header.
  Since the articles do not all depend on the same versions of the same
  packages, each is built in an environment of its own.
- **The scale of each manuscript is set by the layout of its journal's class**
  (`thesis.aastex_twocolumn` or `thesis.spieman`), which is fit inside the
  one-inch margins, not by what is on its pages.
  So a draft is scaled exactly as its final version will be, and whatever
  the class did not put inside its layout, like the line numbers of a draft
  or an equation that runs past its column, shows in the margin.
- **Each manuscript chapter begins** with the Contribution of Authors and
  Co-Authors page and the Manuscript Information page, generated from
  `thesis.manuscripts()`.
- **The headings of each manuscript** are listed in the table of contents,
  from the bookmarks of its PDF, checked against the text of its pages.
- **The cumulative References Cited** merges the bibliographies of the
  manuscripts with `thesis/sources.bib` and cites everything the manuscripts
  cite.

## Building the thesis

Install the package, along with a LaTeX installation with `latexmk`
(TeX Live: `texlive-latex-extra texlive-science cm-super latexmk`):

```bash
pip install -e .[test]
```

Build each manuscript in an environment which has its package installed,
which copies its PDF, formatted bibliography, and BibTeX files into
`thesis/manuscripts/`:

```python
import thesis

for manuscript in thesis.manuscripts():
    manuscript.build(python="path/to/the/environment/of/the/manuscript/python")
```

Then compile the thesis into `thesis/build/thesis.pdf`:

```python
thesis.pdf()
```

The tests build a thesis from two small generated manuscripts, so they need
LaTeX but none of the articles:

```bash
pytest
```

## Still owed

Placeholders render as a bold **XX** or a gray outline, so that the draft
shows plainly what is left.

- [ ] The fullest form of the author's name (first, middle, last) in `thesis/_front.py`.
- [ ] The title, in `thesis/_front.py`.
- [ ] The abstract, introduction, methodology, and conclusion, which the
      Graduate School requires to be solely the student's own writing.
- [ ] The contributions of every author of every manuscript, and the status
      of each manuscript, in `thesis/_manuscripts.py`.
- [ ] The line numbers of each article turned off once it is final.
- [ ] What runs past the layout of its class, into the margin of the thesis,
      fixed in the articles: Eq. 31 and the bottom of page 2 of the noise
      article, and the box AASTeX draws around the caption of the animated
      figure in the event E article, which is 12 big points wider than the
      text.
- [ ] Permission from the publisher of each published manuscript to reproduce it.
- [ ] Confirmation from the Formatting Advisor (gradformatting@montana.edu)
      that the scaled journal pages, whose text is about 9 pt, are acceptable.
- [ ] Alt text for the figures, and the other
      [accessibility requirements](https://www.montana.edu/etd/formatting/accessibility.html).

## License

`thesis/MSUstyle.cls` is the Graduate School's LaTeX class, by Seth Humphries
and maintained by Mark Owkes at
[markowkes/msu-latex](https://bitbucket.org/markowkes/msu-latex) (commit
`3aab2aa376f2`), and is licensed under the
[Creative Commons Attribution-Noncommercial-Share Alike 3.0 License](http://creativecommons.org/licenses/by-nc-sa/3.0/).
