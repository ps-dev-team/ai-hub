---
name: conventions-mobile
description: React Native + TypeScript mobile coding conventions. Use when writing mobile app code. Covers component structure, navigation, platform-specific code, state management, performance, and project structure. Framework-agnostic where possible.
---

# React Native + TypeScript Mobile Conventions

Conventions for mobile app development. Extends the React conventions where applicable — this file covers mobile-specific patterns only.

## Shared with React Conventions

The following apply identically from `conventions-react`:
- Component declaration (`React.FC<Props>`, arrow functions, named exports)
- DRY principles (tokens, enums, constants, types in dedicated directories)
- TypeScript patterns (type everything, zero `any`)
- State management (server vs client, no prop drilling, custom hooks)
- File size limit (~200 lines, then split)
- One component per file

## Platform-Specific Code

### When to Split

Only split by platform when behavior genuinely differs. Don't create `.ios.ts` and `.android.ts` just because you can.

### Patterns

```
// Small differences → inline Platform check
import { Platform } from 'react-native';

const padding = Platform.OS === 'ios' ? 20 : 16;

// Large differences → platform-specific files
Button.ios.tsx
Button.android.tsx
```

### Safe Areas

- Always handle notch, home indicator, and status bar
- Use safe area context — don't hardcode insets
- Test on devices with and without notch

## Navigation

- Keep navigation structure flat where possible
- Type all route params

```typescript
type RootStackParamList = {
  Home: undefined;
  Profile: { userId: string };
  Settings: undefined;
};
```

- Deep linking: define URL scheme in config, not scattered across screens
- Handle back button behavior explicitly on Android

## Styling

- Use `StyleSheet.create()` for static styles — not inline objects
- Design tokens via theme/constants — never hardcode colors or spacing
- Responsive sizing: use relative units or a scaling utility, not fixed pixels
- Dark mode: support from the start via theme system

```typescript
// ✅ Good
const styles = StyleSheet.create({
  container: {
    padding: spacing.md,
    backgroundColor: colors.background,
  },
});

// ❌ Bad
<View style={{ padding: 16, backgroundColor: '#fff' }} />
```

## Performance

### Lists

- Always use `FlatList` or `SectionList` for long lists — never `ScrollView` with `.map()`
- Provide `keyExtractor`
- Use `getItemLayout` when item height is fixed
- Memoize list items with `React.memo`

### Images

- Use correct resolution for device density (@2x, @3x)
- Lazy load off-screen images
- Cache remote images

### Animations

- Prefer `Animated` API or Reanimated for 60fps animations
- Run animations on the native thread where possible
- Avoid layout animations that trigger re-renders

### General

- Avoid unnecessary re-renders (`React.memo`, `useMemo`, `useCallback` where it matters)
- Minimize bridge calls (React Native) — batch when possible
- Profile with Flipper or React DevTools

## Gestures & Interactions

- Touch targets minimum 44x44pt (iOS) / 48x48dp (Android)
- Haptic feedback for important actions (where supported)
- Swipe gestures should have visual affordance
- Handle keyboard: auto-dismiss, avoid overlap with inputs

## Offline & Network

- Assume the network can fail at any time
- Show loading states, error states with retry
- Cache critical data locally
- Queue mutations when offline, sync when back online

## Project Structure

```
src/
├── screens/           # Screen components (one per route)
├── components/        # Shared UI components
├── hooks/             # Shared custom hooks
├── navigation/        # Navigator configs, route types
├── services/          # API calls, business logic
├── utils/             # Shared utilities
├── types/             # Shared TypeScript types
├── constants/         # Colors, spacing, config
├── assets/            # Images, fonts, icons
├── lib/               # External integrations (self-contained)
└── theme/             # Theme config (colors, typography, spacing)
```

## Testing

- Unit test business logic (services, utils, hooks)
- Component tests for key UI states
- E2E with Detox or Maestro for critical user flows
- Test on real devices before release — simulators miss edge cases
