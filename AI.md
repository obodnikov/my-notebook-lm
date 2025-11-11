# AI.md — Guidance for AI Code Assistants

## 📍 Project Context

This repository is a **downstream derivative** of an upstream open-source project.

We intentionally diverged from the upstream codebase to maintain custom logic, integrations, and configurations that are **not fully compatible** with upstream’s structure or policies.  
Direct merges or rebases from upstream are **no longer used**.  
Instead, this repository maintains a **vendor + patch model** for controlled synchronization.

---

## ⚙️ Core Principles

1. **Never modify vendor (upstream) code directly.**
   - The original upstream code lives under:
     ```
     upstream/app/
     ```
   - Treat this directory as **read-only**.  
     Any direct edits here will be overwritten during the next update cycle.

2. **All local changes must be made as patches or extensions.**
   - Store changes under:
     ```
     patches/
     ```
     Each `.patch` file represents a single logical modification.
   - Alternatively, extend functionality via:
     ```
     src/compat/     → compatibility adapters
     src/extensions/ → new modules, plugins, overrides
     ```

3. **Upstream updates are imported, not merged.**
   - The update flow is handled via:
     ```
     ./tools/update_upstream.sh
     ```
   - This script re-imports the latest upstream source into `upstream/app`  
     and reapplies patches automatically.
   - AI tools should never perform `git merge` or `git rebase` operations with upstream.

4. **All patch changes must be generated from diffs.**
   - When suggesting code edits to upstream files, generate patch files:
     ```bash
     git diff upstream/main > patches/XXX-description.patch
     ```
   - The patch must apply cleanly to a fresh copy of `upstream/app`.

5. **Compatibility first.**
   - Prefer writing small adapters or wrappers instead of altering upstream APIs.
   - When upstream introduces breaking changes:
     - Detect version differences.
     - Add compatibility layers in `src/compat/`:
       ```python
       try:
           from upstream.app.api import new_function as func
       except ImportError:
           from upstream.app.api import old_function as func
       ```

---

## 🧩 File Structure Overview

````

myapp-fork/
├── upstream/app/           # read-only copy of original repo
├── patches/                # local patches applied after upstream import
├── src/
│   ├── compat/             # adapters for version differences
│   ├── extensions/         # local functionality
│   └── utils/              # support utilities
├── tools/
│   └── update_upstream.sh  # automation script
└── build.sh                # build pipeline

````
---
## 🧱 Patch organization rule:

Each independent feature, integration, or fix must live in its own subdirectory under patches/.
AI assistants should never aggregate unrelated modifications into a single patch folder.
Patches must remain logically grouped and prefixed numerically for deterministic order.
---

## 🔄 AI Modification Rules

| Task Type | AI Assistant Instruction |
|------------|---------------------------|
| Modify upstream code | ❌ Don’t edit directly — create or update a `.patch` in `patches/` |
| Add feature / fix | ✅ Implement in `src/extensions/` or via patch |
| Adapt to upstream API change | ✅ Add compatibility code in `src/compat/` |
| Update upstream version | ❌ Don’t fetch or rebase; just call `./tools/update_upstream.sh` |
| Fix patch conflict | ✅ Regenerate or adjust the specific `.patch` file |
| Propose improvements | ✅ Create new patch with clear description and commit message |
| Replace old API usage | ✅ Use try/except (Python) or wrapper pattern (TypeScript) |

---

## 🧠 AI Behavior Guidelines

- When the user asks to **“update to latest upstream”**, only modify:
  - `tools/update_upstream.sh` if logic needs improvement.
  - Never modify or directly fetch upstream from AI; just describe the steps.
- When suggesting code changes:
  - Output diff-style snippets or full `.patch` contents.
  - Prefix new patches with sequential numbers (`001-`, `002-`, etc.).
- When generating code inside `src/`, follow project conventions:
  - Python 3.10+, type hints required.
  - TypeScript ES2020+, use async/await where applicable.
  - Keep functions modular and single-purpose.
- When conflicts arise, suggest regenerating the patch, not rebasing.

---

## 🧪 Example: Proper AI Suggestion

**✅ Correct (patch-based change):**
```bash
# AI proposes:
git diff upstream/main > patches/004-fix-logging.patch
````

**✅ Correct (extension-based feature):**

```python
# src/extensions/custom_logger.py
from upstream.app.logging import Logger

class CustomLogger(Logger):
    def info(self, msg):
        super().info("[FORK] " + msg)
```

**❌ Incorrect (direct edit to upstream):**

```python
# upstream/app/logging.py  ❌ Forbidden to edit directly
```

---

## 🔧 Language-Specific Adaptation (TypeScript + Python Hybrid)

### 1. Build & Dependency Model

* **Backend (Python)**
  Uses `pyproject.toml` or `requirements.txt`.
  Build commands via `make build-backend` or `poetry install`.
  Patches affecting Python logic should be created as diffs from files under `upstream/app/server` or similar.

* **Frontend (TypeScript)**
  Built via `npm run build` or `pnpm build`.
  Customizations should live in `src/extensions/ts/` and **never** modify vendor code under `upstream/web/`.

---

### 2. Compatibility Layers

**Python backend**

```python
try:
    from upstream.app.api import new_endpoint as endpoint
except ImportError:
    from upstream.app.routes import endpoint
```

**TypeScript frontend**

```ts
import { api } from "../compat/api";

export function getData() {
  return api.fetch("/v1/data");
}
```

Where `src/compat/api.ts` exports wrappers that normalize upstream API differences.

---

### 3. Code Style

| Language   | Linter / Formatter                | Enforcement    |
| ---------- | --------------------------------- | -------------- |
| Python     | `black`, `ruff`, `mypy`           | `make lint-py` |
| TypeScript | `eslint`, `prettier`              | `npm run lint` |
| CSS        | `stylelint`                       | optional       |
| Jinja      | validated templates, no inline JS | manual         |

AI assistants must ensure any generated code passes these linters before patch creation.

---

### 4. Patch-File Conventions

Patches that modify code should use this filename pattern:

```
patches/
  001-ts-fix-theme-colors.patch
  002-py-add-session-timeout.patch
```

Each patch begins with a short header comment:

```diff
# Patch: Add session timeout support to backend
# Author: AI Assistant (Claude / GPT-5)
# Applies to: upstream/app/server/session.py
```

---

### 5. Docker / Build Integration

* Do **not** rebuild Docker images automatically.
  Only adjust `Dockerfile` if upstream changes break compatibility.
* If the build process needs adaptation, modify `Makefile` targets or add new ones under `make custom-*`.

---

### 6. AI Assistant Behavior Summary

| Action                        | Rule                                                                   |
| ----------------------------- | ---------------------------------------------------------------------- |
| Modify backend logic          | Create `.patch` under `patches/` or new module in `src/extensions/py/` |
| Modify frontend behavior      | Create `.patch` or file in `src/extensions/ts/`                        |
| Add compatibility fix         | Place under `src/compat/` in respective language                       |
| Change build or Docker config | Use patch; document rationale in commit message                        |
| Re-import upstream            | Use `./tools/update_upstream.sh` — never merge                         |

---

## 🔔 Summary for AI Agents

* Treat **`upstream/app/`** as immutable.
* All customizations = `patches/` + `src/extensions/` + `src/compat/`.
* Never rebase or merge upstream; re-import only.
* Always generate patches, adapters, or new modules — never inline edits.
* Preserve structure and comments; clarity > brevity.
* Validate generated code against linters and build targets before suggesting commits.

---

*This `AI.md` is binding for all automated assistants (Claude Code, GPT-5, Codex, etc.) operating on this repository.
Any violation (direct edit in `upstream/`, unauthorized merge, or deletion of patch files) is considered destructive and must be reverted.*
ike me to also generate a small **`.pre-commit-config.yaml`** that enforces these AI rules automatically (linting, patch detection, no direct edits in `upstream/`)?
