# Contributing to MoonPhase Plus

We love your input! We want to make contributing to MoonPhase Plus as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [GitHub Flow](https://guides.github.com/introduction/flow/index.html)
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code follows the style guide.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License
When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/YOUR_USERNAME/moonphase-plus/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/YOUR_USERNAME/moonphase-plus/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Process

### Setting Up Development Environment

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/moonphase-plus.git
   cd moonphase-plus
   ```

2. **Install dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests** to ensure everything works:
   ```bash
   pytest tests/
   ```

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pytest** for testing

Before submitting a PR:
```bash
# Format code
black .

# Check linting
flake8 .

# Check types
mypy .

# Run tests
pytest tests/
```

### Testing

- Write tests for new features
- Ensure existing tests pass
- Add integration tests for complex features
- Test edge cases and error conditions

## Areas for Contribution

### High Priority
1. **New visualization types**
2. **Mobile/desktop apps**
3. **Language translations**
4. **Improved calculation accuracy**
5. **Additional astronomical events**

### Medium Priority
1. **Performance improvements**
2. **More output formats**
3. **Better error handling**
4. **Documentation improvements**
5. **Testing coverage**

### Low Priority
1. **Code refactoring**
2. **Minor bug fixes**
3. **UI/UX improvements**
4. **CI/CD improvements**

## Adding New Features

When adding new features:

1. **Check for existing issues** to avoid duplication
2. **Create a new branch** from `main`
3. **Implement the feature** with tests
4. **Update documentation** (README, docstrings)
5. **Submit a pull request** with clear description

## Documentation

We value good documentation:

- Update README.md for user-facing changes
- Add docstrings to functions and classes
- Update examples if API changes
- Consider writing a blog post about your feature

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

Feel free to:
- Open an issue for questions
- Ask in pull request comments
- Contact the maintainers directly

## Thank You!

Thank you for considering contributing to MoonPhase Plus! Your help makes this tool better for everyone. 🌙

*The MoonPhase Plus Team*