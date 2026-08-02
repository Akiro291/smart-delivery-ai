# Smart Delivery AI - Backend Development Guidelines

## Code Style

- Follow PEP 8 guidelines
- Use type hints throughout
- Maximum line length: 120 characters
- Use async/await for I/O operations
- Follow FastAPI best practices

## Project Structure

```
backend/app/
├── api/           # API endpoints
├── core/          # Core functionality
├── db/           # Database layer
├── modules/      # Business modules
├── services/     # Business logic
├── repositories/ # Data access layer
└── schemas/      # Pydantic schemas
```

## Database

- Use SQLAlchemy 2.0 async API
- Follow domain-driven design principles
- Use migrations for schema changes
- Add indexes for frequently queried fields

## Security

- Hash passwords with bcrypt
- Use JWT for authentication
- Validate all user inputs
- Implement rate limiting
- Use HTTPS in production

## Testing

- Write unit tests for services
- Write integration tests for API endpoints
- Test database operations
- Aim for >80% code coverage

## Deployment

- Use Docker for containerization
- Environment-specific configuration
- Health checks for services
- Graceful shutdown handling

## Performance

- Use async/await throughout
- Implement caching with Redis
- Use connection pooling
- Optimize database queries