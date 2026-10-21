# plotstyle

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
