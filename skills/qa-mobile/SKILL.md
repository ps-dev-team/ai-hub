---
name: qa-mobile
description: QA checklist for mobile app projects (React Native, native iOS/Android). Use after implementing a mobile UI feature or before opening a PR. Covers device testing, visual regression, platform-specific behavior, accessibility, and performance.
---

# QA — Mobile

Post-development quality checklist for mobile app projects.

## When to Run

- After implementing a mobile UI feature
- After addressing review comments on a mobile PR
- Before marking a ticket as Done

## Checklist

### 1. Code Quality

- [ ] No lint errors
- [ ] No type errors
- [ ] Follows project conventions (naming, file structure)
- [ ] Platform-specific code properly separated (when applicable)

### 2. Unit & Component Tests

- [ ] New components have tests
- [ ] Tests cover key states (default, loading, error, empty)
- [ ] Tests cover user interactions
- [ ] All tests pass

### 3. Visual Regression

1. **Capture:** Screenshot on iOS simulator + Android emulator
2. **Compare:** Side-by-side with Figma design
3. **Check:**
   - [ ] Layout matches across both platforms
   - [ ] Typography matches (font, size, weight)
   - [ ] Colors match design tokens
   - [ ] Safe areas respected (notch, home indicator, status bar)
   - [ ] Check at minimum 2 screen sizes per platform:
     - iOS: iPhone SE (375pt), iPhone 15 Pro (393pt)
     - Android: Pixel 5 (393dp), Pixel 7 (412dp)
4. **Document:** Screenshots from both platforms in the PR

Tools: Xcode Simulator, Android Emulator, Maestro for automated screenshots.

### 4. Platform-Specific

**iOS:**
- [ ] Works on minimum supported iOS version
- [ ] No Xcode warnings
- [ ] Dark mode supported (if applicable)
- [ ] Dynamic type / font scaling works

**Android:**
- [ ] Works on minimum supported API level
- [ ] Back button behavior correct
- [ ] Dark mode supported (if applicable)
- [ ] Different screen densities handled (mdpi → xxxhdpi)

### 5. Gestures & Navigation

- [ ] Swipe gestures work correctly
- [ ] Navigation transitions smooth
- [ ] Deep links work (if applicable)
- [ ] Tab bar / bottom nav state correct

### 6. Accessibility

- [ ] Screen reader labels on interactive elements
- [ ] Touch targets minimum 44x44pt (iOS) / 48x48dp (Android)
- [ ] Color contrast meets WCAG AA
- [ ] Focus order logical

### 7. Performance

- [ ] Smooth scrolling (60fps, no jank)
- [ ] App launch time reasonable
- [ ] No memory leaks (monitor in profiler)
- [ ] Images optimized for device resolution
- [ ] List rendering optimized (virtualized lists for long lists)

### 8. Offline & Edge Cases

- [ ] Graceful handling of no network
- [ ] Loading states visible
- [ ] Error states with retry option
- [ ] Keyboard doesn't overlap input fields

## PR Requirements

Before opening the PR:
- [ ] All checklist items above are green
- [ ] Screenshots from iOS + Android attached to PR
- [ ] Figma link in PR description (when applicable)
- [ ] CI passes
