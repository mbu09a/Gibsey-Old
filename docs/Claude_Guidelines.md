# Claude Code Best Practices for Gibsey MVP Sprint

## 1. Prompt Structure for Clean Code Generation

```text
"Generate a FastAPI endpoint for /read that:
- Uses Pydantic models for request/response
- Includes proper error handling with HTTPException
- Has type hints throughout
- Returns JSON with status codes
- Include docstring with endpoint description"
```

## 2. Context Window Management

- Create a `context.md` file with current architecture summary
- Use file paths explicitly: `Update src/api/endpoints/read.py`
- Feed only relevant files: "Given these files: [models.py, database.py], create..."
- Use diff format for changes: "Change lines 15-20 to..."

## 3. React/TypeScript Pattern

```text
"Create a React component using:
- TypeScript with explicit interfaces
- Custom hooks for data fetching
- Error boundaries
- Loading states
- Tailwind classes (no CSS modules yet)"
```

## 4. FastAPI Endpoint Template

```python
# Prompt: "FastAPI endpoint following this pattern:"
@router.post("/endpoint", response_model=ResponseModel)
async def endpoint_name(
    request: RequestModel,
    db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    """Endpoint description."""
    try:
        # Logic here
        return ResponseModel(...)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 5. Database Query Patterns

```text
"Generate SQLAlchemy query that:
- Uses async/await
- Includes proper joins
- Has pagination support
- Returns Pydantic models
- Handles connection pooling"
```

## 6. Embedding Integration

```python
# Prompt template for vector operations
"Create a function that:
- Takes text input
- Calls OpenAI embedding API
- Stores in pgvector column
- Handles API rate limits
- Returns embedding dimension info"
```

## 7. Test Generation Strategy

```text
"Generate Pytest for /read endpoint:
- Mock Supabase responses
- Test error cases
- Use pytest-asyncio
- Include performance assertion (<2s)
- Coverage for all status codes"
```

## 8. Security-First Prompting

```text
"Create config loader that:
- Uses environment variables
- Never hardcodes secrets
- Validates required keys at startup
- Uses pydantic-settings
- Includes .env.example template"
```

## 9. Incremental Update Pattern

```text
"Update the existing function 'get_shard':
- Add parameter 'user_id: str'
- Add logging for timing
- Keep existing error handling
- Show only changed lines"
```

## 10. Performance Instrumentation

```python
# Ask Claude to add timing
"Wrap this function with timing decorator:
@timer_decorator
async def expensive_operation():
    start = time.perf_counter()
    # existing code
    logger.info(f'Operation took {time.perf_counter()-start:.3f}s')
```

## 11. Error Handling Template

```text
"Add comprehensive error handling:
- Supabase connection errors
- OpenAI API timeouts
- Validation errors with details
- Proper status codes
- User-friendly messages"
```

## 12. Component Structure

```typescript
// React component prompt
"Create component with:
interface Props { ... }
const Component: FC<Props> = ({ ... }) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  
  useEffect(() => { ... }, [])
  
  if (loading) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  
  return ( ... )
}"
```

## 13. API Client Pattern

```typescript
"Generate TypeScript API client:
- Axios with interceptors
- Type-safe responses
- Error handling
- Retry logic
- Request/response logging"
```

## 14. Docker Compose Optimization

```text
"Update docker-compose.yml:
- Add health checks
- Set resource limits
- Include wait-for scripts
- Environment variable handling
- Development vs production configs"
```

## 15. CI/CD Pipeline

```yaml
# GitHub Actions prompt
"Create workflow that:
- Runs on PR
- Tests Python & TypeScript
- Checks formatting
- Runs type checking
- Measures coverage
- Fails fast on errors"
```

## 16. Refactoring Request Format

```text
"Refactor this function:
- Extract business logic
- Add type hints
- Reduce complexity
- Improve naming
- Keep same interface"
```

## 17. Database Migration Pattern

```text
"Create Alembic migration:
- Add pgvector extension
- Create pages table with vector column
- Include indexes for performance
- Rollback capability
- Test data in upgrade()"
```

## 18. Common FastAPI Pitfalls

- Always use `async def` for endpoints
- Dependency injection for DB sessions
- Proper CORS configuration
- Request validation with Pydantic
- Background tasks for long operations

## 19. React Performance Checks

```text
"Optimize this component:
- Add React.memo where appropriate
- Use useCallback for handlers
- Implement virtualization for lists
- Lazy load heavy components
- Profile with React DevTools"
```

## 20. Logging Best Practices

```python
"Add structured logging:
logger.info('API called', extra={
    'endpoint': '/read',
    'user_id': user_id,
    'duration_ms': duration,
    'status_code': 200
})"
```

## 21. Environment Configuration

```python
# Pydantic settings prompt
"Create settings class:
class Settings(BaseSettings):
    database_url: PostgresDsn
    openai_api_key: SecretStr
    environment: Literal['dev', 'prod']
    
    class Config:
        env_file = '.env'"
```

## 22. Testing Fixtures

```python
"Generate pytest fixtures:
@pytest.fixture
async def test_client():
    # FastAPI test client setup
    
@pytest.fixture
async def mock_openai():
    # Mock embedding responses"
```

## 23. Type Safety Enforcement

```text
"Add type checking:
- mypy for Python with strict mode
- TypeScript strict: true
- Runtime validation with Pydantic
- Type guards for narrowing"
```

## 24. Code Review Checklist

```text
Before asking Claude to generate:
1. Is the context minimal but complete?
2. Are success criteria clear?
3. Have I specified the style/patterns?
4. Did I mention security constraints?
5. Is the output format specified?
```

## Quick Reference for Tonight

Start each session with:
```text
"I'm working on Week 1 of Gibsey MVP using:
- FastAPI + React + Supabase + pgvector
- Goal: Walking skeleton with /read, /ask, /vault/save
- Current task: [specific task from plan]
- Constraints: <2s round trip, TypeScript strict"
```

Remember: Claude Code works best with specific, bounded requests. Break complex features into smaller, testable chunks.