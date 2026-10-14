import pylatex

__all__ = [
    "abstract",
    "front",
]


def front() -> list[pylatex.NoEscape]:
    """
    The information on the title and copyright pages, and in the properties
    of the PDF.

    The Graduate School asks for the fullest form of the name of the author
    (first, middle, and last) on the title and copyright pages, and for the
    title, author, and language to be set in the properties of the PDF.
    """
    name = "Roy Thomas Smart"
    title = "Computed Tomography Imaging Spectroscopy of the Solar Transition Region"
    return [
        pylatex.NoEscape(rf"\name{{{name}}}"),
        pylatex.NoEscape(rf"\DocTitle{{{title}}}"),
        pylatex.NoEscape(r"\degreetitle{Physics}"),
        pylatex.NoEscape(r"\department{Physics}"),
        pylatex.NoEscape(r"\committeechair{Charles C. Kankelborg}"),
        pylatex.NoEscape(r"\graduationdate{May 2027}"),
        pylatex.NoEscape(r"\copyrightyear{2027}"),
        pylatex.NoEscape(rf"\hypersetup{{pdftitle={{{title}}}, pdfauthor={{{name}}}}}"),
    ]


def abstract() -> pylatex.NoEscape:
    """
    The abstract of the thesis, which the Graduate School asks to be no more
    than 350 words, without formulas or abbreviations, and understandable by
    a reader who is not an expert in the field.

    This is a draft, which the author will rewrite in their own words.
    """
    return pylatex.NoEscape(r"""
\begin{abstract}
The solar transition region, the thin layer between the cool lower atmosphere
of the Sun and its million-degree corona, is threaded by jets and flows that
change within seconds.
Measuring how fast this gas moves requires its spectrum, the brightness of its
light at each wavelength, at every point in an image.
A conventional spectrograph records the spectrum along a narrow slit scanned
across the target, so it cannot see a changing event everywhere at once.
In computed tomography imaging spectroscopy, an instrument without a slit
records several images, each mixing position and wavelength along a different
direction, and a computer reconstructs the spectrum at every point, as a
medical scanner reconstructs a body from many views.
The reconstruction is only as accurate as its model of the instrument,
including how the sensors blur each image and add noise to it.

This dissertation follows that chain from the sensor to the Sun in four
studies.
First, from the tracks of energetic particles crossing the sensors of the
Interface Region Imaging Spectrograph at shallow angles, I measure in orbit how
far charge spreads sideways inside them, which differs by a fifth among
sensors of one design.
Second, I show that ultraviolet images from two space telescopes are less noisy
than standard theory predicts, because some electrons are lost before they can
be counted, so these sensors perform better in the ultraviolet than was
understood.
Third, I describe the Extreme Ultraviolet Snapshot Imaging Spectrograph, which
disperses the image of the Sun in several directions at once, as it was built
and flown on a rocket on 30 September 2019.
Fourth, I reconstruct the spectra of the largest event it observed, a jet in
the quiet Sun, measure flows of up to \textbf{XX} kilometers per second, and
compare them with the magnetic field beneath the jet and with its temperature
of \textbf{XX} million kelvin, measured with several observatories.

\begin{outline}
\item The conclusions, in one or two sentences: what the jet shows about how
  transition region flows are driven, and what the dissertation shows about
  snapshot imaging spectroscopy.
\end{outline}
\end{abstract}""")
