# Einführung in das wissenschaftliche Rechnen (SoSe2024)

## Getting Started

Welcome to the repository for "Einführung in das wissenschaftliche Rechnen"
(Introduction to Scientific Computing) for the Summer Semester 2024 (SoSe2024).

To get started, first clone the
[repository](https://github.com/michaelvanstraten/ewr-so-se-2024) using the
following command:

```sh
git clone https://github.com/michaelvanstraten/ewr-so-se-2024
```

Then, change into the cloned directory with:

```sh
cd ewr-so-se-2024
```

This repository offers two methods for managing dependencies: using
[Poetry](https://python-poetry.org/) or [Nix](https://nixos.org/). Follow the
appropriate section below for setup instructions.

## Setup with [Poetry](https://python-poetry.org/)

[Poetry](https://python-poetry.org/) is a dependency management tool for Python.
Ensure that Poetry is installed and available in your PATH. You can refer to the
[official installation instructions](https://python-poetry.org/docs/#installation)
or follow the steps below if you cannot modify system packages (no root access
required):

```sh
# Install the Poetry package manager
pip install poetry --break-system-packages

# Update the PATH environment variable to include local binaries
export PATH="$HOME/.local/bin:$PATH"

# Install the project's dependencies
poetry install
```

### Running a File in This Repository

To run a module within this repository, use the following command:

```sh
# Execute `python -m ewr_so_se_2024.approximation_of_pi convergence` within the virtual environment.
poetry run python -m ewr_so_se_2024.approximation_of_pi convergence
```

To see what command-line interface (CLI) options are available with each module,
you can add `--help` to the end of the command, like this:

```sh
# Prints help for the `ewr_so_se_2024.approximation_of_pi` module
poetry run python -m ewr_so_se_2024.approximation_of_pi --help
```

The above command will run the
[`__main__.py`](./ewr_so_se_2024/approximation_of_pi/__main__.py) file in this
repository.

### Running Tools like `pylint`

To open an interactive shell with all required dependencies installed, run:

```sh
# Spawn an interactive shell with all dependencies installed
poetry shell
```

Tools like `pylint` (a Python code quality checker) will be available with the
correct versions.

## Setup with [Nix](https://nixos.org/)

[Nix](https://nixos.org/) is a tool for reproducible builds and development
environments. First, install Nix by following the instructions on the
[Nix website](https://nixos.org/download/#download-nix).

To enter a shell defined by the Nix flake (a set of configurations for
reproducible builds), run:

```sh
nix develop
```

After this, you can proceed as described in the Poetry setup section.

## Build a Document with Nix

This repository contains multiple reports and presentations for the assignments
of this course.

To build one of these LaTeX documents using Nix, you can follow the installation
instructions for Nix and then execute the following command:

```sh
nix build github:michaelvanstraten/ewr-so-se-2024#approximation-of-pi-report

```

This command will compile the LaTeX
[`approximation-of-pi/bericht.tex`](./src/approximation-of-pi/bericht.tex)
Document using the configurations specified in the Nix setup.
