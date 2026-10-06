# Contributing to Event Scheduler API

Thank you for your interest in contributing to the Event Scheduler API! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic understanding of Flask and REST APIs

### Setting Up the Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/event-scheduler-api.git
   cd event-scheduler-api
   ```

3. Install dependencies:
   ```bash
   pip install Flask gunicorn
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Use type hints where appropriate

### Project Structure

The project follows a modular architecture:

- `app.py` - Main Flask application and route handlers
- `models.py` - Data models and business entities
- `storage.py` - Data persistence layer
- `validators.py` - Input validation logic
- `templates/` - HTML templates for web interface
- `static/` - CSS and other static assets

### Testing

Before submitting changes:

1. Test all API endpoints using the POSTMAN collection
2. Verify the web interface loads correctly
3. Test edge cases and error conditions
4. Ensure data persistence works correctly

### API Design Principles

- Follow RESTful conventions
- Use appropriate HTTP status codes
- Provide consistent error responses
- Include comprehensive validation
- Maintain backward compatibility

## Making Changes

### Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the guidelines above

3. Test your changes thoroughly

4. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add: new search functionality for events"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a pull request on GitHub

### Commit Message Format

Use clear, descriptive commit messages:

- `Add: new feature or functionality`
- `Fix: bug fix or correction`
- `Update: modification to existing feature`
- `Remove: deletion of code or feature`
- `Docs: documentation changes`

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS)
- Error messages or logs

### Feature Requests

For new features, please provide:

- Clear description of the proposed feature
- Use case and benefits
- Potential implementation approach
- Any breaking changes

### Code Contributions

We welcome contributions for:

- Bug fixes
- New features from the roadmap
- Performance improvements
- Documentation improvements
- Test coverage expansion

## Priority Areas

High-priority areas for contributions:

1. **Testing**: Add unit tests with pytest
2. **Email Notifications**: Implement event reminder emails
3. **Recurring Events**: Add support for repeating events
4. **Database Integration**: Add database backend option
5. **Authentication**: User management and API keys
6. **Time Zones**: Multi-timezone support

## Code Review Process

All contributions go through code review:

1. Automated checks (if implemented)
2. Manual review by maintainers
3. Testing verification
4. Documentation review

### Review Criteria

- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations
- Backward compatibility

## Documentation

When contributing, please update:

- Code comments and docstrings
- README.md if needed
- API documentation
- POSTMAN collection if API changes

## Getting Help

If you need help:

1. Check existing issues and documentation
2. Create an issue for discussion
3. Reach out to maintainers

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the code of conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:

- GitHub contributors list
- Release notes for significant contributions
- README acknowledgments section