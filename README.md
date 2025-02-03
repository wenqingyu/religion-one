# AI Project

A Python-based AI project using modern development practices.

## Setup

This project uses Poetry for dependency management. To get started:

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install basic dependencies:
```bash
poetry install --without ml
```

3. If you need PyTorch and other ML libraries:
```bash
poetry install --with ml
```

4. Activate the virtual environment:
```bash
poetry shell
```

## Alternative Installation Methods

If you're experiencing slow installations, you can try:

1. Installing PyTorch separately using conda or pip
2. Using system-specific PyTorch installations from https://pytorch.org/get-started/locally/

## Project Structure 