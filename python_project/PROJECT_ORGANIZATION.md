# Python Project Organization Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [File Descriptions](#file-descriptions)
4. [Development Workflow](#development-workflow)
5. [Configuration Management](#configuration-management)
6. [Testing Strategy](#testing-strategy)
7. [Documentation Standards](#documentation-standards)
8. [Deployment Guidelines](#deployment-guidelines)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Project Overview

This Python project follows industry-standard conventions and best practices for maintainable, scalable software development. The structure is designed to support both small scripts and large applications with clear separation of concerns.

### Key Principles
- **Modularity**: Code is organized in logical modules and packages
- **Testability**: Every module has corresponding test files
- **Configurability**: Settings are externalized and environment-specific
- **Documentation**: Comprehensive documentation at all levels
- **Version Control**: Git-friendly structure with appropriate ignore patterns

## Directory Structure

```
python_project/
├── src/                    # 📦 Source Code
│   ├── __init__.py        # Package initialization
│   ├── main.py            # Application entry point
│   ├── models/            # Data models and classes
│   ├── services/          # Business logic and services
│   ├── utils/             # Utility functions and helpers
│   └── api/               # API endpoints (if applicable)
├── tests/                  # 🧪 Test Suite
│   ├── __init__.py        # Test package initialization
│   ├── test_main.py       # Main application tests
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test data and fixtures
├── docs/                   # 📚 Documentation
│   ├── README.md          # Documentation overview
│   ├── API.md             # API documentation
│   ├── INSTALL.md         # Installation guide
│   ├── USAGE.md           # Usage examples
│   ├── CONTRIBUTING.md    # Contribution guidelines
│   └── CHANGELOG.md       # Version history
├── scripts/                # 🔧 Utility Scripts
│   ├── setup.py           # Environment setup
│   ├── deploy.py          # Deployment script
│   ├── data_migration.py  # Data migration utilities
│   └── cleanup.py         # Cleanup and maintenance
├── data/                   # 💾 Data Files
│   ├── raw/               # Raw, unprocessed data
│   ├── processed/         # Cleaned and processed data
│   ├── external/          # External data sources
│   └── sample/            # Sample data for testing
├── config/                 # ⚙️ Configuration
│   ├── settings.py        # Application settings
│   ├── logging_config.py  # Logging configuration
│   ├── database.py        # Database configuration
│   └── environments/      # Environment-specific configs
│       ├── development.py
│       ├── testing.py
│       └── production.py
├── logs/                   # 📝 Log Files
│   ├── app_YYYYMMDD.log   # Application logs (auto-generated)
│   ├── error_YYYYMMDD.log # Error logs
│   └── debug_YYYYMMDD.log # Debug logs
├── notebooks/              # 📊 Jupyter Notebooks (optional)
│   ├── exploratory/       # Data exploration
│   ├── analysis/          # Data analysis
│   └── prototyping/       # Feature prototyping
├── assets/                 # 🎨 Static Assets (optional)
│   ├── images/            # Image files
│   ├── templates/         # Template files
│   └── styles/            # Style sheets
├── deployment/             # 🚀 Deployment Files
│   ├── Dockerfile         # Docker configuration
│   ├── docker-compose.yml # Multi-container setup
│   ├── kubernetes/        # Kubernetes manifests
│   └── nginx/             # Web server configuration
├── .github/                # 🔄 GitHub Workflows
│   └── workflows/         # CI/CD pipelines
│       ├── test.yml       # Testing workflow
│       └── deploy.yml     # Deployment workflow
├── requirements.txt        # 📋 Core dependencies
├── requirements-dev.txt    # 🛠️ Development dependencies
├── setup.py               # 📦 Package setup
├── pyproject.toml         # 🔧 Modern Python project config
├── .gitignore             # 🚫 Git ignore patterns
├── .env.example           # 🔐 Environment variables template
├── LICENSE                # ⚖️ License information
├── README.md              # 📖 Project overview
└── PROJECT_ORGANIZATION.md # 📋 This document
```

## File Descriptions

### Core Files

#### `src/main.py`
- **Purpose**: Application entry point
- **Contains**: Main function, CLI argument parsing, application initialization
- **Usage**: `python src/main.py` or `python -m src.main`

#### `requirements.txt`
- **Purpose**: Production dependencies
- **Format**: Package specifications with version constraints
- **Example**:
  ```
  numpy>=1.21.0,<2.0.0
  pandas>=1.3.0
  requests>=2.26.0
  ```

#### `setup.py`
- **Purpose**: Package installation and distribution
- **Contains**: Package metadata, dependencies, entry points
- **Usage**: `pip install -e .` for development installation

### Configuration Files

#### `config/settings.py`
```python
# Environment-specific settings
import os
from typing import Dict, Any

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'
```

#### `config/logging_config.py`
```python
# Centralized logging configuration
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'level': 'DEBUG',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
```

## Development Workflow

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd python_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install project in development mode
pip install -e .
```

### 2. Development Process
1. **Create Feature Branch**: `git checkout -b feature/new-feature`
2. **Write Code**: Implement features in `src/` directory
3. **Write Tests**: Add corresponding tests in `tests/` directory
4. **Run Tests**: `pytest tests/`
5. **Check Code Quality**: `flake8 src/ tests/` and `black src/ tests/`
6. **Update Documentation**: Update relevant documentation
7. **Commit Changes**: `git commit -m "Add new feature"`
8. **Push and Create PR**: `git push origin feature/new-feature`

### 3. Code Quality Checks
```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

## Configuration Management

### Environment Variables
Create `.env` file for local development:
```bash
# .env (not committed to version control)
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///dev.db
API_KEY=your-development-api-key
SECRET_KEY=your-secret-key
```

### Configuration Loading
```python
# config/__init__.py
import os
from .settings import DevelopmentConfig, ProductionConfig

def get_config():
    env = os.getenv('ENVIRONMENT', 'development')
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()

config = get_config()
```

## Testing Strategy

### Test Organization
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Test system performance under load

### Test Structure
```python
# tests/test_example.py
import pytest
from unittest.mock import Mock, patch
from src.example_module import ExampleClass

class TestExampleClass:
    def setup_method(self):
        """Setup for each test method."""
        self.example = ExampleClass()
    
    def test_example_method(self):
        """Test example method with valid input."""
        result = self.example.example_method("test_input")
        assert result == "expected_output"
    
    @pytest.mark.parametrize("input,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
    ])
    def test_example_method_parametrized(self, input, expected):
        """Test example method with multiple inputs."""
        result = self.example.example_method(input)
        assert result == expected
    
    @patch('src.example_module.external_service')
    def test_example_method_with_mock(self, mock_service):
        """Test example method with mocked dependencies."""
        mock_service.return_value = "mocked_response"
        result = self.example.method_using_service()
        assert result == "processed_mocked_response"
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_example.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_example"
```

## Documentation Standards

### Code Documentation
- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Type Hints**: Include type annotations for better code clarity
- **Comments**: Explain complex logic and business rules

### Example Documentation
```python
def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a list of numbers.
    
    Args:
        data: List of numerical values to analyze.
        
    Returns:
        Dictionary containing mean, median, and standard deviation.
        
    Raises:
        ValueError: If data list is empty.
        TypeError: If data contains non-numeric values.
        
    Example:
        >>> data = [1.0, 2.0, 3.0, 4.0, 5.0]
        >>> stats = calculate_statistics(data)
        >>> print(stats['mean'])
        3.0
    """
    if not data:
        raise ValueError("Data list cannot be empty")
    
    # Implementation here...
```

## Deployment Guidelines

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY config/ config/

EXPOSE 8000

CMD ["python", "-m", "src.main"]
```

### Environment-Specific Deployment
- **Development**: Local development server
- **Staging**: Docker containers with staging database
- **Production**: Kubernetes deployment with production database

## Best Practices

### Code Organization
1. **Single Responsibility**: Each module should have one clear purpose
2. **Dependency Injection**: Use dependency injection for better testability
3. **Error Handling**: Implement comprehensive error handling and logging
4. **Configuration**: Externalize all configuration settings

### Security
1. **Environment Variables**: Store sensitive data in environment variables
2. **Input Validation**: Validate all user inputs
3. **Logging**: Log security events but avoid logging sensitive data
4. **Dependencies**: Regularly update dependencies to patch security vulnerabilities

### Performance
1. **Caching**: Implement caching for expensive operations
2. **Database Optimization**: Use proper indexing and query optimization
3. **Async Operations**: Use async/await for I/O-bound operations
4. **Profiling**: Regular performance profiling and optimization

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure project is installed in development mode
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Test Failures
```bash
# Run tests with verbose output
pytest -v --tb=short

# Run specific failing test
pytest tests/test_specific.py::test_specific_function -v
```

#### Environment Issues
```bash
# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Debugging Tips
1. Use `breakpoint()` for interactive debugging
2. Enable debug logging in development
3. Use IDE debugger for step-through debugging
4. Check logs in `logs/` directory for runtime issues

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review and update documentation
- Clean up old log files
- Run security scans
- Performance monitoring

### Version Management
```bash
# Update patch version
# 1.0.0 -> 1.0.1

# Update minor version
# 1.0.1 -> 1.1.0

# Update major version
# 1.1.0 -> 2.0.0
```

---

## Contact and Support

For questions about this project organization:
- Create an issue in the repository
- Contact the development team
- Refer to the contributing guidelines in `docs/CONTRIBUTING.md`

Last updated: June 30, 2025
