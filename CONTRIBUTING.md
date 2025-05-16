# Contributing to Gibsey

Thank you for your interest in contributing to Gibsey! This document outlines the guidelines and best practices for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gibsey.git
   cd gibsey
   ```

2. **Set up the development environment**
   ```bash
   # Start the database
   docker compose up -d db
   
   # Run the setup script
   ./scripts/setup_dev.sh
   ```

## Database Guidelines

### Idempotent Operations

All database operations must be idempotent, meaning they can be run multiple times without causing errors or duplicating data.

1. **Tables**
   - Always use `CREATE TABLE IF NOT EXISTS` when creating tables
   - Include all necessary constraints and indexes in the table definition

2. **Data Insertion**
   - Use `INSERT ... ON CONFLICT DO NOTHING` when inserting data that should be unique
   - Alternatively, check for existence before inserting:
     ```sql
     DO $$
     BEGIN
         IF NOT EXISTS (SELECT 1 FROM table_name WHERE condition) THEN
             INSERT INTO table_name (...) VALUES (...);
         END IF;
     END $$;
     ```

3. **Functions and Procedures**
   - Use `CREATE OR REPLACE FUNCTION` for all function definitions
   - Include proper error handling

## Testing

1. **Running Tests**
   ```bash
   # Run all tests
   pytest
   
   # Run a specific test file
   pytest tests/test_file.py
   ```

2. **Test Database**
   - The test database is automatically reset before each test run
   - Tests should not rely on data from previous tests

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [Black](https://github.com/psf/black) for code formatting
- Include type hints for all function parameters and return values

## Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for your changes
4. Update documentation as needed
5. Run all tests and ensure they pass
6. Submit a pull request with a clear description of your changes

## License

By contributing to Gibsey, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
