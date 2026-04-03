from pathlib import Path

import matplotlib.pyplot as plt

from utils.plotting import save_figure, style_axes


def test_style_axes_sets_common_labels() -> None:
    fig, ax = plt.subplots()

    style_axes(ax, title="Titre", xlabel="X", ylabel="Y")

    assert ax.get_title() == "Titre"
    assert ax.get_xlabel() == "X"
    assert ax.get_ylabel() == "Y"
    plt.close(fig)


def test_save_figure_writes_pdf_file(tmp_path: Path) -> None:
    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 4])

    output = save_figure(fig, "example", directory=tmp_path)

    assert output == tmp_path / "example.pdf"
    assert output.exists()
    plt.close(fig)
