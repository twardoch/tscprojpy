# tscprojpy

A modern Python project template with best practices.

## Features

- 🐍 Python 3.12+ support
- 📦 Modern packaging with `hatchling` and `hatch-vcs`
- 🔧 Dependency management with `uv`
- 🎨 Code formatting and linting with `ruff`
- 🏷️ Automatic versioning from git tags
- 🚀 GitHub Actions CI/CD
- ✅ Testing with `pytest`
- 📊 Code coverage reporting

## Installation

```bash
pip install tscprojpy
```

## Development

```bash
# Clone the repository
git clone https://github.com/twardoch/tscprojpy.git
cd tscprojpy

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv pip install -e .[dev]

# Run tests
uv run pytest

# Run linting
uv run ruff check src tests
uv run ruff format src tests
```

## Usage

```bash
# Show version
tscprojpy version

# Say hello
tscprojpy hello
tscprojpy hello --name="Python"
```

## License

MIT