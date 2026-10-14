from ._chapter import Chapter

__all__ = [
    "introduction",
]


def introduction() -> Chapter:
    """
    The general introduction, which the Graduate School requires and which
    must be solely the student's own writing.
    """
    result = Chapter("Introduction")
    result.append(r"""
\begin{outline}
\item \textbf{The problem context.}
  \begin{itemize}
  \item The solar transition region: between the chromosphere and the corona,
    about $10^4$ to $10^6$\,K, thin and structured by the magnetic field.
  \item Its dynamics: jets, explosive events, and flows, changing in seconds
    to minutes; magnetic reconnection as the proposed driver.
  \item What diagnoses them: the profiles of emission lines formed there,
    such as O\,\textsc{v}, whose shifts, widths, and asymmetries give flows
    and turbulence; needed over a wide field, all at once.
  \item The data cube $I(x, y, \lambda, t)$ against a two-dimensional
    detector, and the ways to flatten it: tunable filters (none in the
    extreme ultraviolet), multilayer imagers (no line profiles), rastered
    slits (IRIS, Hinode/EIS, SPICE; no simultaneity), many slits (MUSE),
    integral field units (SNIFS), and slitless spectrographs, whose
    overlappograms go back to Skylab S082A. A short version of the survey in
    Chapter 5.
  \item Computed tomography imaging spectroscopy: each dispersed order as a
    projection of the cube, and the number of views limiting what can be
    recovered (Kak \& Slaney 1988; Descour et al.\ 1997). Its origins outside
    solar physics (Okamoto \& Yamaguchi 1991; Bulygin et al.\ 1991; Descour
    \& Dereniak 1995), and the terms spectrometer and spectrograph.
  \item The lineage in this group: MOSES (Fox et al.\ 2010; Fox 2011), what
    its flights found (Courrier \& Kankelborg 2018; Rust \& Kankelborg 2019;
    Parker \& Kankelborg 2022) and where its design binds, then ESIS (the
    earlier design in Courrier 2020; the first flight in Parker et al.\
    2022).
  \item Why the sensors matter: a reconstruction inverts a model of the
    instrument, so errors in the model become artifacts in the spectra.
    \begin{itemize}
    \item The blur of the sensor, from charge diffusion, belongs in the point
      spread function of the model.
    \item The noise of the sensor sets how closely a reconstruction should
      fit the images (for example, stopping at $\chi^2 \approx 1$) and the
      uncertainty of what it recovers.
    \item Both are rarely measured on a flight sensor; ESIS flew
      back-illuminated CCDs whose quantum efficiency was not measured
      before flight (Chapter 5).
    \item Why Chapters 3 and 4 use sensors on IRIS and the Hubble Space
      Telescope rather than those of ESIS, and how their results carry over.
    \end{itemize}
  \end{itemize}
\item \textbf{The purpose and objectives.}
  \begin{itemize}
  \item The purpose: tomographic imaging spectroscopy of the transition
    region, carried from the sensor to a measurement of the Sun.
  \item To measure how back-illuminated sensors blur an image, in orbit.
  \item To explain the noise of back-illuminated sensors in the
    ultraviolet.
  \item To describe ESIS as it was built and flown, and how its design
    answers the limitations of MOSES.
  \item To measure the flows, magnetic topology, and temperature of a
    transition region jet with ESIS.
  \end{itemize}
\item \textbf{How the manuscripts address them.}
  \begin{itemize}
  \item Chapter 2: the methods common to the manuscripts, in more detail
    than they had room for.
  \item Chapters 3 to 6: for each manuscript, the question it answers, what
    it found, and what the next chapter takes from it. The chapters are in
    the order of publication, so none refers forward.
    \begin{itemize}
    \item Chapter 3: the charge-diffusion kernel of the IRIS sensors, from
      glancing particle tracks.
    \item Chapter 4: partial charge collection, and the noise of
      ultraviolet images from IRIS and the Hubble Space Telescope.
    \item Chapter 5: ESIS, its design, and its first flight.
    \item Chapter 6: event E, a jet observed by ESIS.
    \end{itemize}
  \item Chapter 7: the conclusion.
  \end{itemize}
\end{outline}""")
    return result
