# AI Guidelines for TypeScript Project

This file defines how AI assistants should generate or modify code in this repository.
The goal: keep output consistent, type-safe, production-ready, and aligned with modern TypeScript and project conventions.

---

## General Rules

* Follow **TypeScript ESLint** and **Prettier** formatting conventions.
* Always **enable strict typing** (`"strict": true` in `tsconfig.json`).
* Use **explicit types** for all variables, parameters, and function returns.
* Include **JSDoc comments** (`/** ... */`) for functions, classes, and modules.
* Use **arrow functions** for inline and callback logic, and **named functions** for exported utilities.
* Prefer **template literals** for string formatting.
* Use **async/await** instead of Promise chains for readability.
* Avoid silent failures — handle errors with descriptive messages.

---

## Project Structure

* Avoid large, monolithic files; keep each module focused (~500–800 lines max).
* Place main source code in `src/`, tests in `tests/`, and scripts/utilities in `scripts/`.
* Keep configuration files in the root (`tsconfig.json`, `.env`, `config.yaml`).
* **Never hard-code secrets or credentials**. Load from environment variables or secure config.
* Keep test files **only** in `tests/` directory.
* Keep **all documentation files**, except `README.md`, in a separate `docs/` directory.

---

## Dependencies

* Use `package.json` to manage dependencies.
* Prefer built-in Node.js APIs or lightweight utilities before adding third-party packages.
* When adding a new dependency, briefly explain why it’s required (in PR or comments).
* Use `import` syntax (`import fs from 'fs'`) — avoid `require`.

---

## Error Handling

* Centralize and standardize error handling in a shared utility or base class.
* Use **custom error classes** (`class AppError extends Error { ... }`) for domain-specific failures.
* Always log errors with a proper logger (e.g., `winston`, `pino`) instead of `console.log`.
* Include clear context in error messages.

---

## Testing

* Use **Jest** or **Vitest** for unit and integration tests.
* Test all public APIs, utilities, and core logic.
* Keep tests deterministic; avoid network or file system dependencies unless mocked.
* Maintain one test file per module (`<module>.test.ts`).

---

## Examples

✅ **Good:**

```typescript
export const loadData = async (path: string): Promise<string[]> => {
  /** Load a text file and split lines safely */
  if (!fs.existsSync(path)) {
    throw new Error(`File not found: ${path}`);
  }
  const data = await fs.promises.readFile(path, 'utf-8');
  return data.split('\n');
};
```

❌ **Bad:**

```typescript
function loaddata(p) {
  return fs.readFileSync(p).split('\n'); // no error handling, untyped
}
```

---

## Code Review and AI Output Expectations

* The AI assistant must:

  * Generate clean, lint-free TypeScript code.
  * Use modern syntax (`const`, `let`, `async/await`, ES modules).
  * Ensure generated code compiles without TypeScript errors.
  * Keep comments concise but informative.
  * Never disable type checking (`// @ts-ignore`) unless absolutely necessary, and explain why.

---
