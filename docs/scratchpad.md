# Scratchpad

## Edge Cases / Open Questions

- tRPC `section` and `symbol` routes assume backend endpoints `/sections` and `/symbol` which do not yet exist.
- Page navigation expects sequential numeric IDs; gaps will show errors.
- Color theme uses custom Tailwind colors `background` and `terminal`; other components may need updates for contrast.

## Manual Checks

- **Chrome 124** on Linux: components render, navigation and search update page content.
- **Firefox 125** on Linux: same behaviour observed; no layout issues.
