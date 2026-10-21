"""House plot style for LaTeX documents and the website, in light and dark.

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
