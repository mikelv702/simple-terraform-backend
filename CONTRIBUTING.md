# Contributing to simple-terraform-backend

We're excited that you're interested in contributing to the simple-terraform-backend project! This document outlines the process for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/terraform-fastapi-backend.git
   cd terraform-fastapi-backend
   ```
3. Create a new branch for your feature or bug fix:
   ```
   git checkout -b feature/your-feature-name
   ```

## Setting Up the Development Environment

1. Ensure you have Python 3.7+ installed.
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the development dependencies:
   ```
   pip install -r requirements.txt
   ```

## Making Changes

1. Make your changes in your feature branch.
2. Add or update tests as necessary.
3. Ensure all tests pass:
   ```
   pytest
   ```
4. Update documentation if you've made changes to the API or added new features.

## Commit Guidelines

- Use clear and meaningful commit messages.
- Reference issue numbers in your commit messages if applicable.
- Make sure each commit represents a logical unit of change.

## Submitting a Pull Request

1. Push your changes to your fork on GitHub:
   ```
   git push origin feature/your-feature-name
   ```
2. Go to the original project repository on GitHub and create a new Pull Request.
3. Describe your changes in detail, referencing any related issues.
4. Wait for a maintainer to review your PR. They may ask for changes or clarifications.

## Code Style

- Follow PEP 8 guidelines for Python code.
- Use type hints where possible.
- Document your functions and classes using docstrings.

## Testing

- Write unit tests for new functionality.
- Ensure all existing tests pass before submitting a PR.
- Aim for high test coverage for new code.

## Documentation

- Update the README.md if you've made changes that affect how the project is used.
- Document new features or changes to existing features in the appropriate places.

## Reporting Bugs

- Use the GitHub Issues tracker to report bugs.
- Describe the bug in detail, including steps to reproduce.
- Include information about your environment (OS, Python version, etc.).

## Requesting Features

- Use the GitHub Issues tracker to suggest new features.
- Clearly describe the feature and its potential benefits.
- Be open to discussion about the feature's implementation.

## Questions?

If you have any questions about contributing, feel free to open an issue for clarification.
