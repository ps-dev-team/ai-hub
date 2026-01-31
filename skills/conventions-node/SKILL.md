---
name: conventions-node
description: Node.js + TypeScript backend coding conventions. Use when writing APIs, services, or backend code. Covers layered architecture, error handling, validation, project structure, and best practices. Framework-agnostic.
---

# Node.js + TypeScript Backend Conventions

Framework-agnostic conventions for backend projects.

## Architecture

Layered architecture — each layer has a single responsibility:

```
Routes → Controllers → Services → Repositories → Database
```

| Layer | Responsibility | Depends On |
|---|---|---|
| **Routes** | Define endpoints, input validation, auth middleware | Controllers |
| **Controllers** | Orchestrate request/response, call services | Services |
| **Services** | Business logic, pure functions where possible | Repositories |
| **Repositories** | Data access (DB queries, external API calls) | Database / APIs |

### Rules

- Services never import from routes or controllers
- Repositories never contain business logic
- Controllers don't access the database directly
- Changing the framework (Express → Fastify) only affects routes/controllers

## Project Structure

```
src/
├── routes/            # Endpoint definitions + middleware wiring
├── controllers/       # Request orchestration
├── services/          # Business logic
├── repositories/      # Data access (DB, external APIs)
├── middleware/         # Auth, error handling, logging, validation
├── models/            # Database models / schemas
├── types/             # Shared TypeScript types
├── utils/             # Shared utilities
├── config/            # Environment config, constants
├── lib/               # External integrations (self-contained)
│   └── stripe/        # Example: payment provider
└── index.ts           # Entry point
```

## TypeScript

- Type everything — zero `any`
- Named exports only
- Arrow functions
- Request/response types defined per endpoint
- Shared types in `src/types/`

```typescript
type CreateUserRequest = {
  email: string;
  name: string;
  role: 'admin' | 'user';
};

type CreateUserResponse = {
  id: string;
  email: string;
  createdAt: string;
};
```

## Error Handling

### Centralized Error Middleware

One error handler for the entire app — no try/catch in every controller:

```typescript
// Custom error classes
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, `${resource} not found`, 'NOT_FOUND');
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(400, message, 'VALIDATION_ERROR');
  }
}
```

### Error Response Format

Consistent error shape across all endpoints:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

### Async Handler

Wrap async route handlers to catch errors automatically:

```typescript
const asyncHandler = (fn: Function) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
```

## Validation

- Validate all input at the route/controller level — before it reaches services
- Use schema validation (Zod, Joi, etc.) — not manual checks
- Return clear, specific error messages
- Validate request body, query params, and path params

```typescript
// Example with Zod
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['admin', 'user']),
});
```

## API Design

- RESTful endpoints: `GET /users`, `POST /users`, `GET /users/:id`
- Consistent naming: plural nouns for resources
- Proper HTTP status codes: 200, 201, 204, 400, 401, 403, 404, 500
- Pagination for list endpoints: `?page=1&limit=20`
- Version prefix when needed: `/api/v1/`

## Environment & Config

- All config from environment variables — never hardcoded
- Single config file that validates env vars at startup:

```typescript
// src/config/index.ts
export const config = {
  port: parseInt(process.env.PORT || '3000'),
  databaseUrl: requireEnv('DATABASE_URL'),
  jwtSecret: requireEnv('JWT_SECRET'),
};
```

- Fail fast: if a required env var is missing, crash at startup — not at runtime

## Logging

- Structured logging (JSON format in production)
- Log levels: error, warn, info, debug
- Log request/response in middleware (method, path, status, duration)
- Never log sensitive data (passwords, tokens, PII)
- Include request ID for tracing

## Security

- Validate and sanitize all input
- Use parameterized queries — never string concatenation for SQL
- Rate limiting on public endpoints
- CORS configured explicitly — no wildcard in production
- Secrets in environment variables, never in code
- Auth middleware on protected routes

## DRY

Same principle as frontend:
- Shared types in `src/types/`
- Shared utils in `src/utils/`
- Constants in `src/config/` or `src/constants/`
- External integrations isolated in `src/lib/`
