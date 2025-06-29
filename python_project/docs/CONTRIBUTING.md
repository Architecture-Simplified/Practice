# Contributing to Python Project

We welcome contributions to this project! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/python-project.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
5. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
6. Install pre-commit hooks: `pre-commit install`

## Development Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 2. Make Changes
- Write your code in the `src/` directory
- Add tests in the `tests/` directory
- Update documentation if needed
- Follow the coding standards below

### 3. Test Your Changes
```bash
# Run tests
pytest

# Check code coverage
pytest --cov=src --cov-report=html

# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "Add feature: brief description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Coding Standards

### Code Style
- Use [Black](https://black.readthedocs.io/) for code formatting
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function parameters and return values
- Maximum line length: 88 characters

### Documentation
- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Include examples in docstrings when helpful
- Update README.md if adding new features

### Testing
- Write tests for all new functionality
- Aim for at least 80% code coverage
- Use descriptive test names
- Group related tests in classes

### Example Code Style
```python
def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numerical values.
        
    Returns:
        The arithmetic mean of the numbers.
        
    Raises:
        ValueError: If the list is empty.
        
    Example:
        >>> calculate_average([1.0, 2.0, 3.0])
        2.0
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    return sum(numbers) / len(numbers)
```

## Pull Request Guidelines

### Before Submitting
- [ ] All tests pass
- [ ] Code coverage is maintained or improved
- [ ] Code is formatted with Black
- [ ] No linting errors
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)

### Pull Request Description
Include:
- Brief description of changes
- Related issue number (if applicable)
- Screenshots (for UI changes)
- Breaking changes (if any)

### Review Process
1. Automated checks must pass
2. At least one code review is required
3. All feedback must be addressed
4. Maintainer will merge after approval

## Issue Reporting

### Bug Reports
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests
Include:
- Clear description of the feature
- Use case and motivation
- Possible implementation approach

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Unacceptable Behavior
- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing private information
- Spam or off-topic content

## Getting Help

- Check existing issues and documentation
- Ask questions in GitHub discussions
- Contact maintainers directly for sensitive issues

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- Release notes

Thank you for contributing to our project!
