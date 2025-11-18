# Contributing to Money Marketing Tool

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Code Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions
- Maximum line length: 100 characters
- Use Black for formatting
- Use isort for import sorting

### TypeScript (Frontend)
- Follow React best practices
- Use functional components with hooks
- Type all props and state
- Use meaningful variable names
- Follow the existing code structure

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=src
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## Questions?

Open an issue or join our Discord community.
