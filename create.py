"""Run this once: it creates the plotstyle/ package folder next to this script."""
from pathlib import Path

FILES = {}

FILES['plotstyle/README.md'] = r'''# plotstyle

House matplotlib styles for LaTeX documents and the website, in light and dark.

## Install (once)

Put this folder anywhere, e.g. `~/code/plotstyle`, then from inside whatever
environment your projects use:

    pip install -e ~/code/plotstyle

`-e` (editable) means changes you make to the style files take effect
immediately, with no reinstall. After this, `import plotstyle` works from any
folder or subfolder of any project using that environment.

## Use

    import plotstyle

    plotstyle.use("latex")              # targets: "latex", "web"
    plotstyle.use("web", theme="dark")  # themes:  "light", "dark"

    fig, ax = plotstyle.figure()        # frac=0.5 for half-width figures
    ax.plot(x, y)
    plotstyle.save(fig, "figures/name") # latex -> .pdf, web -> .svg + .png

Every version at once (plotting goes in a function so it can be redrawn
under each style):

    def make():
        fig, ax = plotstyle.figure()
        ax.plot(x, y)
        return fig

    plotstyle.render(make, "figures/name")
    # name_latex_light.pdf, name_web_light.svg/.png, name_web_dark.svg/.png

One-off tweaks: `plotstyle.use("web", rc={"axes.grid": False})`, or
temporarily: `with plotstyle.context("web", "dark"): ...`

Plain matplotlib also works:
`plt.style.use(["plotstyle.base", "plotstyle.web", "plotstyle.dark"])`

## Files

| file              | contents                                            |
|-------------------|-----------------------------------------------------|
| `base.mplstyle`   | layout, spines, sizes shared by everything          |
| `latex.mplstyle`  | Computer Modern fonts, embedded fonts in PDFs       |
| `web.mplstyle`    | Verdana, SVG text left as live text                 |
| `light.mplstyle`  | Okabe-Ito palette on white                          |
| `dark.mplstyle`   | lightened palette on `#1E1E1E` (set to your site's) |

## Notes

- For Computer Modern text (not just maths) install the CMU Serif font, or set
  `text.usetex: True` in `latex.mplstyle` if you have a TeX install.
  Otherwise text falls back to DejaVu Serif.
- To size LaTeX figures exactly, set the width in `base.mplstyle` to your
  document's `\textwidth` in inches (`\the\textwidth` prints it in pt;
  divide by 72.27), and include figures with `width=\textwidth` or no scaling.
- Web SVGs keep text as text, so browsers draw it in Verdana even if Verdana
  isn't installed where the plot was made.
'''

FILES['plotstyle/pyproject.toml'] = r'''[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[project]
name = "plotstyle"
version = "0.1.0"
description = "House matplotlib styles for LaTeX and the web, light and dark"
requires-python = ">=3.9"
dependencies = ["matplotlib>=3.7"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
plotstyle = ["*.mplstyle"]
'''

FILES['plotstyle/src/plotstyle/__init__.py'] = r'''"""House plot style for LaTeX documents and the website, in light and dark.

Basic use, from any folder of any project once installed:

    import plotstyle
    plotstyle.use("latex")                 # or "web", theme="dark"
    fig, ax = plotstyle.figure()
    ax.plot(x, y)
    plotstyle.save(fig, "figures/myplot")  # .pdf for latex, .svg for web

To make every version of a figure at once, put the plotting in a function:

    def make():
        fig, ax = plotstyle.figure()
        ax.plot(x, y)
        return fig

    plotstyle.render(make, "figures/myplot")
    # -> myplot_latex_light.pdf, myplot_web_light.svg, myplot_web_dark.svg

The styles can also be used with plain matplotlib:
    plt.style.use(["plotstyle.base", "plotstyle.web", "plotstyle.dark"])
"""
from contextlib import contextmanager
from importlib.resources import files
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

__all__ = ["use", "context", "figure", "save", "render", "style_list"]

TARGETS = ("latex", "web")
THEMES = ("light", "dark")
DEFAULT_FORMATS = {"latex": ("pdf",), "web": ("svg", "png")}
DEFAULT_RENDERS = (("latex", "light"), ("web", "light"), ("web", "dark"))

_current = {"target": "latex", "theme": "light"}


def _path(name):
    return str(files(__package__) / f"{name}.mplstyle")


def style_list(target="latex", theme="light"):
    """Paths of the style sheets for a target and theme, in apply order."""
    if target not in TARGETS:
        raise ValueError(f"target must be one of {TARGETS}, got {target!r}")
    if theme not in THEMES:
        raise ValueError(f"theme must be one of {THEMES}, got {theme!r}")
    return [_path("base"), _path(target), _path(theme)]


def use(target="latex", theme="light", rc=None):
    """Apply the style globally. `rc` is an optional dict of rcParams to
    override, e.g. use("web", rc={"axes.grid": False})."""
    mpl.rcdefaults()
    plt.style.use(style_list(target, theme))
    mpl.rcParams.update(rc or {})
    _current.update(target=target, theme=theme)


@contextmanager
def context(target="latex", theme="light", rc=None):
    """Apply the style only inside a `with` block."""
    previous = dict(_current)
    with plt.style.context(style_list(target, theme), after_reset=True):
        mpl.rcParams.update(rc or {})
        _current.update(target=target, theme=theme)
        try:
            yield
        finally:
            _current.update(previous)


def figure(nrows=1, ncols=1, frac=1.0, aspect=None, **kwargs):
    """plt.subplots sized from the style.

    frac   -- fraction of the default width (0.5 for side-by-side figures).
    aspect -- height / width; defaults to the style's ratio, scaled by grid shape.
    """
    w, h = mpl.rcParams["figure.figsize"]
    width = w * frac
    if aspect is None:
        aspect = (h / w) * nrows / ncols ** 0.5
    return plt.subplots(nrows, ncols, figsize=(width, width * aspect), **kwargs)


def save(fig, name, formats=None, close=False):
    """Save a figure, by default in the formats suited to the current target.
    Creates parent folders as needed. Returns the list of paths written."""
    formats = formats or DEFAULT_FORMATS[_current["target"]]
    stem = Path(name)
    stem.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for ext in formats:
        path = stem.with_name(f"{stem.name}.{ext}")
        fig.savefig(path)
        written.append(path)
    if close:
        plt.close(fig)
    return written


def render(make, name, versions=DEFAULT_RENDERS, formats=None):
    """Call `make()` (which must return a figure) once per (target, theme)
    and save each as name_target_theme.ext. Styles have to be in place when
    a figure is drawn, which is why the plotting goes in a function."""
    written = []
    for target, theme in versions:
        with context(target, theme):
            fig = make()
            written += save(fig, f"{name}_{target}_{theme}", formats, close=True)
    return written
'''

FILES['plotstyle/src/plotstyle/base.mplstyle'] = r'''# Shared layout: no colours, no fonts. Combine with a target and a theme.

figure.figsize:              6.4, 4.0
figure.dpi:                  110
figure.constrained_layout.use: True

font.size:        11
axes.labelsize:   11
axes.titlesize:   12
legend.fontsize:  10
xtick.labelsize:  10
ytick.labelsize:  10

axes.spines.top:   False
axes.spines.right: False
axes.linewidth:    0.8
axes.grid:         True
grid.linewidth:    0.6
grid.alpha:        0.25

xtick.direction:   out
ytick.direction:   out
xtick.major.size:  3.5
ytick.major.size:  3.5
xtick.major.width: 0.8
ytick.major.width: 0.8

lines.linewidth:   1.8
lines.markersize:  5

legend.frameon:    False

savefig.dpi:       300
savefig.bbox:      tight
savefig.pad_inches: 0.03
'''

FILES['plotstyle/src/plotstyle/dark.mplstyle'] = r'''# Dark theme. Okabe-Ito reordered and lightened so every colour reads on a
# dark background (black swapped for light grey, dark blue moved later and
# brightened).

axes.prop_cycle: cycler('color', ['56B4E9', 'E69F00', '35C4A0', 'FF7F50', 'E58FC3', '6FA8FF', 'F0E442', 'DDDDDD'])

# Change these three to match your site's background colour exactly.
figure.facecolor:  1E1E1E
axes.facecolor:    1E1E1E
savefig.facecolor: 1E1E1E

text.color:        E6E6E6
axes.labelcolor:   E6E6E6
axes.edgecolor:    AAAAAA
xtick.color:       AAAAAA
ytick.color:       AAAAAA
grid.color:        BBBBBB
legend.labelcolor: E6E6E6
'''

FILES['plotstyle/src/plotstyle/latex.mplstyle'] = r'''# For figures included in LaTeX documents.
# Computer Modern text and maths so labels match the surrounding document.

font.family:      serif
font.serif:       CMU Serif, Computer Modern Roman, DejaVu Serif
mathtext.fontset: cm
axes.formatter.use_mathtext: True

# Embed fonts as TrueType (Type 42) rather than Type 3; journals and
# arXiv prefer it and text stays selectable.
pdf.fonttype: 42
ps.fonttype:  42

# Set to True for exact LaTeX rendering (needs a TeX install; slower).
text.usetex: False
'''

FILES['plotstyle/src/plotstyle/light.mplstyle'] = r'''# Light theme. Okabe-Ito palette (colour-blind safe).

axes.prop_cycle: cycler('color', ['0072B2', 'E69F00', '009E73', 'D55E00', 'CC79A7', '56B4E9', 'F0E442', '000000'])

figure.facecolor:  white
axes.facecolor:    white
savefig.facecolor: white

text.color:        222222
axes.labelcolor:   222222
axes.edgecolor:    444444
xtick.color:       444444
ytick.color:       444444
grid.color:        888888
legend.labelcolor: 222222
'''

FILES['plotstyle/src/plotstyle/web.mplstyle'] = r'''# For figures on the website (Verdana body text).

font.family:      sans-serif
font.sans-serif:  Verdana, DejaVu Sans, Bitstream Vera Sans, sans-serif
mathtext.fontset: dejavusans

# Verdana is wide; slightly smaller sizes keep tick labels from crowding.
font.size:        10
axes.labelsize:   10
axes.titlesize:   11
legend.fontsize:  9
xtick.labelsize:  9
ytick.labelsize:  9

# Keep text as real text in SVGs, so the browser draws it in the site's own
# Verdana even if Verdana isn't installed where the plot was made.
svg.fonttype: none
'''

for path, text in FILES.items():
    p = Path(__file__).parent / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    print("wrote", p)
