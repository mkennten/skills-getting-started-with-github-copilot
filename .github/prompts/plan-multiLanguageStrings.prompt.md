## Plan: Add Multi-Language Strings (i18n)

Introduce a lightweight JSON-dictionary i18n layer used by both the FastAPI backend and the vanilla JS frontend. Add locale negotiation (query param + `Accept-Language` + fallback), replace hard-coded UI/API strings with translation keys, and keep English as the default so existing behavior (and most tests) stays stable. Keep activity IDs stable to avoid breaking API clients/tests, and optionally add localized display fields later.

### Steps
1. Inventory strings and define translation keys for UI + API messages in `src/app.py`, `src/static/index.html`, and `src/static/app.js`.
2. Add locale dictionaries (e.g., `en`, `es`) and a small backend helper (e.g., `negotiate_locale()`, `t(key, **params)`) loaded at startup from the i18n folder.
3. Implement language negotiation on the backend (priority: `lang` query param → cookie → `Accept-Language` → `en`) and switch API responses/exceptions in `src/app.py` to translated strings.
4. Update the frontend to load the chosen dictionary on startup, replace JS-rendered strings in `src/static/app.js`, and send the locale to the API (via `Accept-Language` header and/or `?lang=`).
5. Update assertions in `tests/test_app.py` to either rely on default English or explicitly set a locale header when asserting exact strings; ensure no tests depend on localized activity “names” as keys.

### Further Considerations
1. Single source of truth for dictionaries: serve JSON via backend (shared) vs keep under static (simpler); which do you prefer?
2. Do you want activity names/descriptions localized now, or only system messages (errors/success/UI labels) first to avoid API-breaking changes?
