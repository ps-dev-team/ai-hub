---
name: qa-backend
description: QA checklist for backend projects. Use after implementing an API endpoint, service, or data layer change. Covers unit tests, integration tests, API contract validation, security, and performance.
---

# QA — Backend

Post-development quality checklist for backend projects.

## When to Run

- After implementing an API endpoint or service
- After changing data models or database schemas
- Before opening a PR with backend changes

## Checklist

### 1. Code Quality

- [ ] No lint errors
- [ ] No type errors
- [ ] No unused imports or dead code
- [ ] Follows project conventions (naming, file structure, error handling)

### 2. Unit Tests

- [ ] New functions/methods have tests
- [ ] Tests cover happy path
- [ ] Tests cover edge cases (empty input, invalid data, boundaries)
- [ ] Tests cover error handling (exceptions, error responses)
- [ ] All tests pass

### 3. Integration Tests

- [ ] API endpoints return correct status codes
- [ ] Request/response payloads match API contract
- [ ] Database operations work correctly (CRUD)
- [ ] External service integrations handled (mocked or sandboxed)

### 4. API Contract Validation

- [ ] Endpoint paths follow conventions (RESTful, consistent naming)
- [ ] Request validation rejects invalid input with clear error messages
- [ ] Response format matches documented schema
- [ ] Pagination works correctly (when applicable)
- [ ] Auth/permissions enforced on protected endpoints

### 5. Data Integrity

- [ ] Database migrations run cleanly (up and down)
- [ ] No data loss on schema changes
- [ ] Indexes added for frequently queried fields
- [ ] Foreign keys and constraints in place

### 6. Security

- [ ] No secrets hardcoded (use environment variables)
- [ ] Input sanitized (SQL injection, XSS prevention)
- [ ] Auth tokens validated
- [ ] Rate limiting configured (when applicable)
- [ ] Sensitive data not logged

### 7. Performance

- [ ] No N+1 query problems
- [ ] Database queries optimized (explain plan)
- [ ] Response times reasonable under expected load
- [ ] No memory leaks in long-running processes

## PR Requirements

Before opening the PR:
- [ ] All checklist items above are green
- [ ] Test coverage maintained or improved
- [ ] CI passes
- [ ] API documentation updated (when applicable)
