"""
This is the main executable script.

It can be executed by running `python3 ./simulation/main.py`
"""

from core import print_hi
from mesa_example import run_mesa_example, plot_mesa_example
import matplotlib.pyplot as plt
from pathlib import Path


def main() -> None:
    # Usage of the `print_hi` function defined in `core.py`
    print_hi("Python script")

    # This is an example of importing simulation code, executing it and plotting it in a python script. The simulation
    # takes 245 iterations and about 3 minutes.
    run_data = run_mesa_example()

    fig, ax = plt.subplots()
    plot_mesa_example(run_data, ax)

    # The plot is written to a file.
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    plt.savefig(results_dir / "mesa-example-gini.pdf")


if __name__ == '__main__':
    main()
