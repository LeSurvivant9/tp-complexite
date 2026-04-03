from pathlib import Path

import matplotlib.axes
import matplotlib.figure

FIGURES_DIR = Path(__file__).resolve().parent.parent / "docs" / "figures"


def style_axes(
    ax: matplotlib.axes.Axes,
    *,
    title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    if ax.get_legend_handles_labels()[0]:
        ax.legend(fontsize=10)
    ax.grid(True, which="both", alpha=0.3, linestyle="--")
    ax.tick_params(axis="both", labelsize=9)


def save_figure(
    fig: matplotlib.figure.Figure,
    stem: str,
    *,
    directory: Path = FIGURES_DIR,
) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / f"{stem}.pdf"
    fig.savefig(output, bbox_inches="tight")
    return output
