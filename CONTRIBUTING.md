# Contributing Guidelines

Thank you for considering contributing to the Python-React Boilerplate!

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Use the issue template
3. Provide clear reproduction steps
4. Include environment details (OS, Python version, etc.)

### Submitting Changes

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests if applicable
   - Update documentation

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Run linters**
   ```bash
   flake8 .
   black .
   isort .
   ```

6. **Commit your changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```
   
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting)
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Use the PR template
   - Link related issues
   - Describe your changes clearly

## Code Style Guidelines

### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 88 characters (Black default)
- Use docstrings for functions and classes

**Example:**
```python
from typing import List

def get_users(page: int = 1, page_size: int = 20) -> List[dict]:
    """
    Get paginated list of users.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
    
    Returns:
        List of user dictionaries
    """
    # Implementation
    pass
```

### JavaScript/React

- Use ES6+ syntax
- Functional components with hooks
- Use meaningful variable names
- Add JSDoc comments for complex functions

**Example:**
```javascript
/**
 * Fetch user data from API
 * @param {number} userId - User ID
 * @returns {Promise<Object>} User object
 */
async function fetchUser(userId) {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}
```

## Testing Guidelines

### Backend Tests

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_authentication():
    """Test user authentication flow."""
    # Register
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    })
    assert response.status_code == 201
    
    # Login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Frontend Tests

```javascript
import { render, screen } from '@testing-library/react';
import Login from './Login';

test('renders login form', () => {
  render(<Login />);
  const emailInput = screen.getByLabelText(/email/i);
  expect(emailInput).toBeInTheDocument();
});
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions
- Update architecture diagrams if needed
- Include code examples for new features

## Review Process

1. Automated checks must pass (linting, tests)
2. At least one maintainer review required
3. Address review comments
4. Squash commits if requested
5. Maintainer will merge when approved

## Community Guidelines

- Be respectful and constructive
- Help others learn
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Ask questions if unclear

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/python-react-boilerplate.git
   cd python-react-boilerplate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.fastapi.txt
   pip install -r requirements-dev.txt
   ```

4. **Setup pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## Questions?

- Open an issue for discussion
- Join our community chat (if available)
- Email maintainers

Thank you for contributing! 🎉
