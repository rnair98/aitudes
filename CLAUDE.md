# Aitudes Development Guidelines

## Commands
- Format code: `black .`
- Type check: `mypy .`
- Run tests: `pytest`
- Run specific test: `pytest path/to/test.py::test_function`

## Code Style
- **Imports**: Standard library → third-party → project imports
- **Formatting**: Use Black with 4-space indentation and 80-char line limit
- **Types**: Use comprehensive type annotations with Pydantic for validation
- **Naming**: snake_case (variables/functions), CamelCase (classes), UPPER_CASE (constants)
- **Error Handling**: Provide descriptive error messages with context information
- **Documentation**: Docstrings for all classes and functions

## Clean Code Principles
- Write single-responsibility functions that do one thing well
- Use meaningful variable/function names that explain intent
- Avoid magic numbers and hardcoded values
- Follow DRY principle and continuously refactor
- Encapsulate complex conditionals in well-named functions

## AI Assistant Guidelines
When working with this codebase:
1. Analyze the context thoroughly before making changes
2. Decompose problems into clear steps
3. Follow established code patterns and conventions
4. Provide coherent changes that maintain type safety
5. Document the purpose and limitations of your changes