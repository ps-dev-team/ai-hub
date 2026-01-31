---
name: conventions-react
description: React + TypeScript coding conventions. Use when writing React components, hooks, or frontend code. Covers component structure, state management, TypeScript patterns, styling, error handling, and project organization.
---

# React + TypeScript Conventions

## Component Structure

### File Organization

- One component per file
- Single file is fine up to ~200 lines — split after that
- Types live next to the component, not in a separate file (unless shared)
- Named exports only — no default exports

### Component Declaration

```tsx
export const UserCard: React.FC<UserCardProps> = ({ name, avatar, role }) => {
  return (
    <div>
      {/* ... */}
    </div>
  );
};
```

- Arrow functions, always
- Props destructured in the signature
- Types declared directly above or next to the component

### Splitting Large Components

When a file exceeds ~200 lines:
- Extract logic into a custom hook (`useUserCard.ts`)
- Extract sub-components into separate files
- Keep the main component as the orchestrator

## DRY

- **Colors, spacing, sizes** → design tokens (Tailwind config or CSS variables), never hardcoded
- **Enums** → `src/enums/` directory
- **Constants / configs** → `src/constants/` directory
- **Shared types** → `src/types/` directory
- **Shared utils** → `src/utils/` directory
- If you use something in more than one place, extract it

## State Management

### Separation of Concerns

- **Server state** (data fetching, cache) — separate from UI state, use data fetching libs
- **Client/UI state** (modals, forms, toggles) — local `useState` or custom hooks

### Where State Lives

| Scope | Solution |
|---|---|
| Single component | `useState` |
| Component + children (2 levels max) | Props |
| Subtree (3+ levels) | React Context |
| Global / complex | External state lib |

### Rules

- **No prop drilling** beyond 2 levels — use Context or a store
- Encapsulate state logic in custom hooks (`useAuth`, `useCart`, etc.)
- Keep state as close to where it's used as possible

## TypeScript

- Use `type` or `interface` — whichever fits. No strict preference, just be consistent per project.
- Type everything — aim for zero `any`. Good DX depends on autocomplete working.
- Export types when other files need them
- Props types colocated with the component:

```tsx
type UserCardProps = {
  name: string;
  avatar: string;
  role: 'admin' | 'user';
};

export const UserCard: React.FC<UserCardProps> = ({ name, avatar, role }) => {
  // ...
};
```

## Styling

- **Utility-first CSS** (Tailwind) as the default for web
- **Headless component libraries** (Radix, etc.) for accessible UI primitives
- **No CSS-in-JS runtime** (styled-components, emotion) — incompatible with SSR, dying ecosystem
- Design tokens via Tailwind config — never hardcode colors or spacing in components
- Animation libraries (Framer Motion, etc.) for motion

## Error Handling

### Error Boundaries

Wrap major sections of the app with error boundaries to prevent full-page crashes:

```tsx
<ErrorBoundary fallback={<ErrorFallback />}>
  <Dashboard />
</ErrorBoundary>
```

### Async Operations

- Try/catch in async functions inside hooks or event handlers
- Always handle the error state in UI (loading → success → error)
- Show user-friendly error messages with retry option

### Side Effects

- Minimize `useEffect` — prefer event handlers when possible
- Every `useEffect` must have correct dependencies
- Cleanup subscriptions and timers in the return function
- If `useEffect` logic is complex, extract to a custom hook

## Project Structure

Hybrid approach — base by type, integrations isolated:

```
src/
├── components/        # Shared UI components
├── hooks/             # Shared custom hooks
├── utils/             # Shared utilities
├── types/             # Shared types
├── enums/             # Shared enums
├── constants/         # Shared constants / configs
├── lib/               # External integrations (self-contained)
│   ├── prismic/       # Example: CMS integration
│   │   ├── components/
│   │   └── api/
│   └── stripe/        # Example: payment integration
│       ├── components/
│       └── api/
├── app/               # Routes / pages (Next.js App Router, etc.)
└── styles/            # Global styles, Tailwind entry
```

### Integration Folders (`lib/`)

- Each integration is self-contained and portable
- Has its own `components/`, `api/`, `hooks/` as needed
- Can be moved to another project with minimal changes
