---
name: qa-frontend
description: QA checklist for frontend web projects. Use after implementing a UI feature or before opening a PR that includes visual changes. Covers unit tests, component tests, e2e, visual regression against Figma, accessibility, and performance.
---

# QA — Frontend Web

Post-development quality checklist for frontend web projects.

## When to Run

- After implementing a UI feature, before opening a PR
- After addressing review comments on a UI PR
- Before marking a ticket as Done

## Checklist

### 1. Code Quality

- [ ] No lint errors (`npm run lint` / `bun run lint`)
- [ ] No type errors (`tsc --noEmit`)
- [ ] No unused imports or dead code
- [ ] Component follows project conventions (naming, file structure)

### 2. Unit & Component Tests

- [ ] New components have tests
- [ ] Tests cover key states (default, loading, error, empty)
- [ ] Tests cover user interactions (click, input, submit)
- [ ] All tests pass (`npm test` / `bun test`)

### 3. Visual Regression — Figma Comparison

This is the most critical check for UI work:

1. **Capture:** Screenshot the implemented component/page in the browser
2. **Compare:** Place screenshot side-by-side with the Figma design
3. **Check:**
   - [ ] Layout matches (spacing, alignment, proportions)
   - [ ] Typography matches (font, size, weight, line-height, color)
   - [ ] Colors match design tokens
   - [ ] Border radius, shadows, and effects match
   - [ ] Responsive: check at mobile (375px), tablet (768px), desktop (1280px+)
4. **Document:** Include before/after or design/implementation screenshots in the PR

Tools: browser DevTools, screenshot capture, Figma overlay comparison.

### 4. Cross-Browser

- [ ] Chrome (primary)
- [ ] Firefox
- [ ] Safari (if targeting macOS/iOS)

### 5. Accessibility

- [ ] Semantic HTML (headings, landmarks, buttons vs divs)
- [ ] Alt text on images
- [ ] Keyboard navigation works (tab order, focus states)
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 large text)
- [ ] No Lighthouse accessibility errors

### 6. Performance

- [ ] No unnecessary re-renders (React DevTools profiler)
- [ ] Images optimized (correct format, lazy loading)
- [ ] Bundle size reasonable (no unexpected large imports)
- [ ] Lighthouse performance score > 90

### 7. E2E Tests (when applicable)

- [ ] Critical user flows covered
- [ ] Tests pass in CI
- [ ] No flaky tests introduced

## PR Requirements

Before opening the PR:
- [ ] All checklist items above are green
- [ ] Screenshots attached to PR (mandatory for UI changes)
- [ ] Figma link in PR description (when applicable)
- [ ] CI passes
