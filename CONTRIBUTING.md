# Contributing to NessHash

Thank you for your interest in contributing to NessHash! We welcome all forms of contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Rust (latest stable version)
- Git
- [Poetry](https://python-poetry.org/) (Python dependency management)
- [Cargo](https://doc.rust-lang.org/cargo/) (Rust package manager)

### Setting Up the Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/NessHash.git
   cd NessHash
   git remote add upstream https://github.com/MKWorldWide/NessHash.git
   ```

2. **Set Up Python Environment**
   ```bash
   # Install Python dependencies
   poetry install
   
   # Activate the virtual environment
   poetry shell
   ```

3. **Set Up Rust Environment**
   ```bash
   # Install Rust if you haven't already
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   
   # Add Rust to your PATH
   source $HOME/.cargo/env
   
   # Install Rust components
   rustup component add rustfmt clippy
   ```

4. **Install Pre-commit Hooks**
   ```bash
   # Install pre-commit
   pip install pre-commit
   
   # Install git hooks
   pre-commit install
   ```

## Development Workflow

1. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. **Make Your Changes**
   - Follow the code style guidelines (see below)
   - Write tests for new features
   - Update documentation as needed

3. **Run Tests and Linters**
   ```bash
   # Python tests
   pytest
   
   # Rust tests
   cargo test
   
   # Linting
   pre-commit run --all-files
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
   
   Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

5. **Push and Create a Pull Request**
   ```bash
   git push origin your-branch-name
   ```
   Then create a pull request from your fork to the main repository.

## Code Style

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all new code
- Keep lines under 100 characters
- Use `black` for code formatting
- Use `isort` for import sorting
- Use `flake8` for linting
- Use `mypy` for static type checking

### Rust
- Follow the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- Use `rustfmt` for code formatting
- Use `clippy` for linting
- Document all public items with `///` doc comments

## Documentation

- Update the documentation when adding new features or changing existing ones
- Use Markdown for all documentation
- Follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings
- Keep the `docs/` directory up to date

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Aim for good test coverage (80%+)
- Use descriptive test names that explain what's being tested

## Reporting Issues

When reporting issues, please include:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. Environment details (OS, Python/Rust versions, etc.)
5. Any relevant error messages or logs

## Code Review Process

1. A maintainer will review your pull request
2. You may be asked to make changes or provide additional information
3. Once approved, your changes will be merged into the main branch

## License

By contributing to NessHash, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE.md).

## Questions?

If you have any questions, feel free to open an issue or reach out to the maintainers.
